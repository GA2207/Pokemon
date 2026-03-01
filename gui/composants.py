"""
gui/composants.py - Composants Pygame reutilisables pour l'interface Pokemon.
Boutons, barres de vie, champ texte, liste scrollable, badges de type.
"""

import pygame
from type_chart import TYPE_COLORS
from config import (COULEUR_TEXTE, COULEUR_TEXTE_GRIS, COULEUR_FOND_CLAIR,
                    COULEUR_FOND_CARTE)


# ─── Bouton ───────────────────────────────────────────────────────────────────

class Bouton:
    """Bouton cliquable avec survol."""

    def __init__(self, x, y, largeur, hauteur, texte, couleur,
                 couleur_texte=COULEUR_TEXTE, taille_police=16, enabled=True):
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.texte = texte
        self.couleur = couleur
        self.couleur_hover = tuple(min(255, c + 30) for c in couleur)
        self.couleur_texte = couleur_texte
        self.taille_police = taille_police
        self.enabled = enabled
        self._survol = False

    def handle_event(self, event):
        """Retourne True si le bouton est clique."""
        if not self.enabled:
            return False
        if event.type == pygame.MOUSEMOTION:
            self._survol = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def draw(self, surface):
        if not self.enabled:
            couleur = (80, 80, 80)
            couleur_txt = (120, 120, 120)
        elif self._survol:
            couleur = self.couleur_hover
            couleur_txt = self.couleur_texte
        else:
            couleur = self.couleur
            couleur_txt = self.couleur_texte

        pygame.draw.rect(surface, couleur, self.rect, border_radius=6)
        font = pygame.font.SysFont("Arial", self.taille_police, bold=True)
        txt_surf = font.render(self.texte, True, couleur_txt)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        surface.blit(txt_surf, txt_rect)


# ─── Barre de vie ────────────────────────────────────────────────────────────

class BarreVieWidget:
    """Barre de vie avec gradient de couleur."""

    VERT = (22, 163, 74)
    JAUNE = (234, 179, 8)
    ROUGE = (220, 38, 38)

    def __init__(self, x, y, largeur=250, hauteur=20):
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self._largeur = largeur
        self._hauteur = hauteur

    def draw(self, surface, pv, pv_max):
        if pv_max <= 0:
            return
        ratio = max(0, min(1, pv / pv_max))
        largeur_rempli = int(self._largeur * ratio)

        if ratio > 0.5:
            couleur = self.VERT
        elif ratio > 0.2:
            couleur = self.JAUNE
        else:
            couleur = self.ROUGE

        # Fond
        pygame.draw.rect(surface, (74, 74, 74), self.rect, border_radius=4)
        # Barre
        if largeur_rempli > 0:
            bar_rect = pygame.Rect(self.rect.x, self.rect.y,
                                   largeur_rempli, self._hauteur)
            pygame.draw.rect(surface, couleur, bar_rect, border_radius=4)
        # Texte PV
        font = pygame.font.SysFont("Arial", 12, bold=True)
        txt = font.render(f"{pv}/{pv_max}", True, COULEUR_TEXTE)
        txt_rect = txt.get_rect(center=self.rect.center)
        surface.blit(txt, txt_rect)


# ─── Badge de type ────────────────────────────────────────────────────────────

def dessiner_badge_type(surface, type_nom, x, y):
    """Dessine un badge de type colore. Retourne la largeur occupee."""
    couleurs = TYPE_COLORS.get(type_nom, {"rgb": (136, 136, 136)})
    couleur = couleurs["rgb"]

    font = pygame.font.SysFont("Arial", 11, bold=True)
    txt_surf = font.render(type_nom, True, COULEUR_TEXTE)
    w = txt_surf.get_width() + 12
    h = txt_surf.get_height() + 6

    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(surface, couleur, rect, border_radius=4)
    surface.blit(txt_surf, (x + 6, y + 3))
    return w + 4


# ─── Champ de texte ──────────────────────────────────────────────────────────

class ChampTexte:
    """Champ de saisie de texte simple."""

    def __init__(self, x, y, largeur=250, hauteur=32, placeholder=""):
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.texte = ""
        self.placeholder = placeholder
        self.actif = False
        self._curseur_visible = True
        self._curseur_timer = 0

    def handle_event(self, event):
        """Retourne True si le texte a change."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.actif = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.actif:
            if event.key == pygame.K_BACKSPACE:
                self.texte = self.texte[:-1]
                return True
            elif event.key == pygame.K_RETURN:
                self.actif = False
            elif event.unicode and event.unicode.isprintable():
                self.texte += event.unicode
                return True
        return False

    def draw(self, surface):
        couleur_bord = (100, 160, 255) if self.actif else (100, 100, 100)
        pygame.draw.rect(surface, COULEUR_FOND_CLAIR, self.rect, border_radius=4)
        pygame.draw.rect(surface, couleur_bord, self.rect, 2, border_radius=4)

        font = pygame.font.SysFont("Arial", 14)
        if self.texte:
            txt_surf = font.render(self.texte, True, COULEUR_TEXTE)
        else:
            txt_surf = font.render(self.placeholder, True, COULEUR_TEXTE_GRIS)
        surface.blit(txt_surf, (self.rect.x + 8, self.rect.y + 7))


# ─── Liste scrollable ────────────────────────────────────────────────────────

class ListeScrollable:
    """Liste d'items avec scroll et selection."""

    def __init__(self, x, y, largeur, hauteur, hauteur_item=28):
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self._items = []
        self._hauteur_item = hauteur_item
        self._scroll_offset = 0
        self._selection = -1
        self._font = pygame.font.SysFont("Courier New", 13)

    def set_items(self, items):
        """items = liste de strings."""
        self._items = items
        self._scroll_offset = 0
        self._selection = -1

    def get_selection(self):
        """Retourne l'index selectionne ou -1."""
        return self._selection

    def handle_event(self, event):
        """Retourne True si la selection change."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if event.button == 1:
                    # Clic gauche : selection
                    rel_y = event.pos[1] - self.rect.y + self._scroll_offset
                    idx = rel_y // self._hauteur_item
                    if 0 <= idx < len(self._items):
                        self._selection = idx
                        return True
                elif event.button == 4:  # Scroll up
                    self._scroll_offset = max(0, self._scroll_offset - 30)
                elif event.button == 5:  # Scroll down
                    max_scroll = max(0, len(self._items) * self._hauteur_item - self.rect.height)
                    self._scroll_offset = min(max_scroll, self._scroll_offset + 30)
        elif event.type == pygame.MOUSEWHEEL:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self._scroll_offset -= event.y * 30
                max_scroll = max(0, len(self._items) * self._hauteur_item - self.rect.height)
                self._scroll_offset = max(0, min(max_scroll, self._scroll_offset))
        return False

    def draw(self, surface):
        # Fond
        pygame.draw.rect(surface, COULEUR_FOND_CLAIR, self.rect, border_radius=4)

        # Clip
        clip_rect = surface.get_clip()
        surface.set_clip(self.rect)

        visible_start = self._scroll_offset // self._hauteur_item
        visible_end = min(len(self._items),
                          visible_start + self.rect.height // self._hauteur_item + 2)

        for i in range(visible_start, visible_end):
            y = self.rect.y + i * self._hauteur_item - self._scroll_offset

            if y + self._hauteur_item < self.rect.y or y > self.rect.y + self.rect.height:
                continue

            # Fond de selection
            if i == self._selection:
                sel_rect = pygame.Rect(self.rect.x, y, self.rect.width, self._hauteur_item)
                pygame.draw.rect(surface, (69, 123, 157), sel_rect)

            # Texte
            txt_surf = self._font.render(self._items[i], True, COULEUR_TEXTE)
            surface.blit(txt_surf, (self.rect.x + 8, y + 5))

        surface.set_clip(clip_rect)

        # Bordure
        pygame.draw.rect(surface, (80, 80, 80), self.rect, 1, border_radius=4)

        # Scrollbar indicateur
        if len(self._items) * self._hauteur_item > self.rect.height:
            total_h = len(self._items) * self._hauteur_item
            bar_h = max(20, int(self.rect.height * self.rect.height / total_h))
            bar_y = self.rect.y + int(self._scroll_offset / total_h * self.rect.height)
            bar_rect = pygame.Rect(self.rect.right - 8, bar_y, 6, bar_h)
            pygame.draw.rect(surface, (100, 100, 100), bar_rect, border_radius=3)


# ─── Zone de log ──────────────────────────────────────────────────────────────

class ZoneLog:
    """Zone de texte read-only pour les messages de combat."""

    def __init__(self, x, y, largeur, hauteur):
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self._messages = []
        self._font = pygame.font.SysFont("Courier New", 12)
        self._scroll_offset = 0
        self._line_height = 18

    def ajouter(self, message):
        if message and message.strip():
            self._messages.append(message.strip())
            # Auto-scroll vers le bas
            total_h = len(self._messages) * self._line_height
            if total_h > self.rect.height:
                self._scroll_offset = total_h - self.rect.height

    def ajouter_plusieurs(self, messages):
        for msg in messages:
            self.ajouter(msg)

    def handle_event(self, event):
        if event.type == pygame.MOUSEWHEEL:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self._scroll_offset -= event.y * 20
                max_scroll = max(0, len(self._messages) * self._line_height - self.rect.height)
                self._scroll_offset = max(0, min(max_scroll, self._scroll_offset))

    def draw(self, surface):
        pygame.draw.rect(surface, COULEUR_FOND_CLAIR, self.rect, border_radius=4)

        clip_rect = surface.get_clip()
        surface.set_clip(self.rect)

        for i, msg in enumerate(self._messages):
            y = self.rect.y + 4 + i * self._line_height - self._scroll_offset
            if y + self._line_height < self.rect.y or y > self.rect.y + self.rect.height:
                continue
            txt_surf = self._font.render(msg, True, (200, 200, 200))
            surface.blit(txt_surf, (self.rect.x + 8, y))

        surface.set_clip(clip_rect)
        pygame.draw.rect(surface, (80, 80, 80), self.rect, 1, border_radius=4)
