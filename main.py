import pygame
import json
import combat

# 1) CONFIG
SCREEN_WIDTH = 1560
SCREEN_HEIGHT = 960
FPS = 60

JSON_PATH = "pokemon.json"

# Palette "Nintendo premium" (vert profond + or)
C_BG_TOP = (5, 28, 25)
C_BG_BOTTOM = (3, 18, 16)

C_PANEL = (8, 45, 38)
C_PANEL_INNER = (10, 55, 46)
C_PANEL_BORDER = (190, 152, 62)

C_RING_1 = (20, 106, 92)
C_RING_2 = (190, 152, 62)

C_BTN = (18, 72, 60)
C_BTN_2 = (14, 56, 48)
C_BTN_HOVER = (28, 108, 92)
C_BTN_TEXT = (245, 242, 230)
C_ACCENT = (190, 152, 62)

C_TEXT_SOFT = (205, 197, 170)
C_SHADOW = (0, 0, 0)

pygame.init()

# 2) DATA

def charger_pokemons(path=JSON_PATH):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, list) else data.get("pokemon", [])

def filtrer_par_gen(pokemons, gen_mode):
    if gen_mode == "gen1":
        return [p for p in pokemons if 1 <= p.get("numero", 0) <= 151]
    if gen_mode == "gen2":
        return [p for p in pokemons if 152 <= p.get("numero", 0) <= 251]
    if gen_mode == "gen12":
        return [p for p in pokemons if 1 <= p.get("numero", 0) <= 251]
    return pokemons

import random
import os

def choisir_trainer(gen_mode):
    base = "assets/sprites/trainers"

    if gen_mode == "gen1":
        candidats = [f for f in os.listdir(base) if "gen1" in f]
    elif gen_mode == "gen2":
        candidats = [f for f in os.listdir(base) if "gen2" in f]
    else:
        candidats = os.listdir(base)

    if not candidats:
        return None

    return os.path.join(base, random.choice(candidats))

# 3) VISUELS (dégradé + texture)

def draw_rounded_rect(surface, rect, color, radius=16, width=0):
    pygame.draw.rect(surface, color, rect, border_radius=radius, width=width)

def draw_vertical_gradient(surface, top_color, bottom_color):
    w, h = surface.get_size()
    for y in range(h):
        t = y / max(h - 1, 1)
        r = int(top_color[0] * (1 - t) + bottom_color[0] * t)
        g = int(top_color[1] * (1 - t) + bottom_color[1] * t)
        b = int(top_color[2] * (1 - t) + bottom_color[2] * t)
        pygame.draw.line(surface, (r, g, b), (0, y), (w, y))

def draw_subtle_texture(surface, alpha=18, step=6):
    """
    Texture premium très légère (grain + diagonales).
    """
    w, h = surface.get_size()
    tex = pygame.Surface((w, h), pygame.SRCALPHA)

    # Grain discret
    for y in range(0, h, step):
        for x in range(0, w, step):
            a = alpha if (x + y) % (step * 2) == 0 else alpha // 2
            tex.fill((255, 255, 255, a), pygame.Rect(x, y, 1, 1))

    # Diagonales très faibles
    for i in range(-h, w, 28):
        pygame.draw.line(tex, (255, 255, 255, alpha // 3), (i, 0), (i + h, h), 1)

    surface.blit(tex, (0, 0))

def dessiner_pokeball(surface, center, r=12, accent=C_ACCENT, line=(20, 20, 20)):
    x, y = center
    pygame.draw.circle(surface, (235, 232, 220), (x, y), r)
    top_rect = pygame.Rect(x - r, y - r, 2 * r, r)
    pygame.draw.ellipse(surface, accent, top_rect)
    pygame.draw.line(surface, line, (x - r, y), (x + r, y), 3)
    pygame.draw.circle(surface, (245, 242, 230), (x, y), r // 3 + 2)
    pygame.draw.circle(surface, line, (x, y), r // 3 + 2, 2)
    pygame.draw.circle(surface, line, (x, y), r, 2)

# =========================
# 4) BOUTON
# =========================
class Bouton:
    def __init__(self, x, y, w, h, texte, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.texte = texte
        self.est_survole = False
        self.font = font

    def verifier_survol(self, pos_souris):
        self.est_survole = self.rect.collidepoint(pos_souris)

    def dessiner(self, surface):
        # Ombre (propre)
        shadow = self.rect.move(6, 6)
        draw_rounded_rect(surface, shadow, (0, 0, 0), radius=18)

        base = C_BTN_HOVER if self.est_survole else C_BTN
        draw_rounded_rect(surface, self.rect, base, radius=18)

        inner = self.rect.inflate(-10, -10)
        inner_col = (34, 130, 108) if self.est_survole else C_BTN_2
        draw_rounded_rect(surface, inner, inner_col, radius=14)

        # Bordure premium fine
        border_col = C_ACCENT if self.est_survole else (230, 225, 205)
        draw_rounded_rect(surface, self.rect, border_col, radius=18, width=3)

        txt = self.font.render(self.texte, True, C_BTN_TEXT)
        txt_rect = txt.get_rect(center=self.rect.center)
        surface.blit(txt, txt_rect)

# =========================
# 5) JEU
# =========================
class Jeu:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pokémon - La Plateforme")
        self.clock = pygame.time.Clock()

        self.font_title = pygame.font.SysFont("impact", 110)
        self.font_sub = pygame.font.SysFont("impact", 34)
        self.font_btn = pygame.font.SysFont("impact", 30)
        self.font_info = pygame.font.SysFont("impact", 26)

        self.etat_actuel = "menu"
        self.pokemons = charger_pokemons()
        self.gen_mode = "gen1"

        # Panneau : on l’agrandit pour que tout rentre (c'était le bug)
        self.panel_w = 820
        self.panel_h = 820
        self.panel_rect = pygame.Rect(
            (SCREEN_WIDTH - self.panel_w) // 2,
            (SCREEN_HEIGHT - self.panel_h) // 2 + 10,
            self.panel_w,
            self.panel_h
        )

        self._creer_boutons()

    def _creer_boutons(self):
        # Layout auto : tout rentre DANS le panneau, quoi qu’il arrive
        x = self.panel_rect.x + 170
        w = self.panel_rect.w - 340
        h = 64

        top_margin = 210   # espace pour titre + sous-titre
        bottom_margin = 70
        y_start = self.panel_rect.y + top_margin
        y_end = self.panel_rect.bottom - bottom_margin

        # Total 7 boutons -> on calcule gap pour que ça rentre
        total_buttons = 7
        usable_h = y_end - y_start
        gap = (usable_h - total_buttons * h) // (total_buttons - 1)
        gap = max(gap, 14)  # minimum pour que ça respire

        self.boutons_menu = {}
        order = [
            ("gen1",  "GEN 1"),
            ("gen2",  "GEN 2"),
            ("gen12", "GEN 1+2"),
            ("jouer",   "LANCER UNE PARTIE"),
            ("ajouter", "AJOUTER UN POKÉMON"),
            ("pokedex", "ACCÉDER AU POKÉDEX"),
            ("quitter", "QUITTER"),
        ]

        y = y_start
        for key, label in order:
            self.boutons_menu[key] = Bouton(x, y, w, h, label, self.font_btn)
            y += h + gap

    def dessiner_fond(self):
        draw_vertical_gradient(self.screen, C_BG_TOP, C_BG_BOTTOM)
        draw_subtle_texture(self.screen, alpha=16, step=6)

        centre = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
        pygame.draw.circle(self.screen, C_RING_1, centre, 430, 10)
        pygame.draw.circle(self.screen, C_RING_2, centre, 300, 6)
        pygame.draw.circle(self.screen, C_RING_1, centre, 190, 6)
        pygame.draw.line(self.screen, C_RING_1, (centre[0] - 520, centre[1]), (centre[0] + 520, centre[1]), 6)

    def dessiner_panel(self):
        # Glow discret
        glow = self.panel_rect.inflate(12, 12)
        draw_rounded_rect(self.screen, glow, (0, 0, 0), radius=30)

        draw_rounded_rect(self.screen, self.panel_rect, C_PANEL, radius=28)
        draw_rounded_rect(self.screen, self.panel_rect, C_PANEL_BORDER, radius=28, width=3)

        inner = self.panel_rect.inflate(-18, -18)
        draw_rounded_rect(self.screen, inner, C_PANEL_INNER, radius=22, width=2)

        # Micro texture dans le panneau (premium)
        panel_tex = pygame.Surface((inner.w, inner.h), pygame.SRCALPHA)
        for i in range(0, inner.w + inner.h, 34):
            pygame.draw.line(panel_tex, (255, 255, 255, 10), (i, 0), (i - inner.h, inner.h), 1)
        self.screen.blit(panel_tex, (inner.x, inner.y))

    def afficher_menu(self):
        self.dessiner_fond()
        self.dessiner_panel()

        # Titre + ombre
        title_shadow = self.font_title.render("POKÉMON", True, C_SHADOW)
        title = self.font_title.render("POKÉMON", True, C_ACCENT)

        cx = SCREEN_WIDTH // 2
        ty = self.panel_rect.y + 80
        rect = title.get_rect(center=(cx, ty))
        self.screen.blit(title_shadow, rect.move(4, 4))
        self.screen.blit(title, rect)

        sub = self.font_sub.render("Choisissez votre génération", True, C_TEXT_SOFT)
        sub_rect = sub.get_rect(center=(cx, self.panel_rect.y + 135))
        self.screen.blit(sub, sub_rect)

        # Mode actuel (top-left)
        mode_txt = self.font_info.render(f"Mode actuel : {self.gen_mode.upper()}", True, C_TEXT_SOFT)
        self.screen.blit(mode_txt, (48, 36))
        dessiner_pokeball(self.screen, (28, 48), r=12)

        # Boutons + Pokéball au survol (SEULEMENT au survol)
        for btn in self.boutons_menu.values():
            btn.dessiner(self.screen)
            if btn.est_survole:
                dessiner_pokeball(self.screen, (btn.rect.x - 26, btn.rect.centery), r=12)

    def gestion_evenements(self):
        pos = pygame.mouse.get_pos()

        if self.etat_actuel == "menu":
            for btn in self.boutons_menu.values():
                btn.verifier_survol(pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.etat_actuel != "menu":
                    return

                if self.boutons_menu["gen1"].rect.collidepoint(pos):
                    self.gen_mode = "gen1"
                elif self.boutons_menu["gen2"].rect.collidepoint(pos):
                    self.gen_mode = "gen2"
                elif self.boutons_menu["gen12"].rect.collidepoint(pos):
                    self.gen_mode = "gen12"

                elif self.boutons_menu["jouer"].rect.collidepoint(pos):
                    liste = filtrer_par_gen(self.pokemons, self.gen_mode)
                    combat.lancer_combat(liste)

                elif self.boutons_menu["quitter"].rect.collidepoint(pos):
                    pygame.quit()
                    raise SystemExit

                # ajouter / pokedex : à brancher ensuite

    def run(self):
        while True:
            self.gestion_evenements()
            if self.etat_actuel == "menu":
                self.afficher_menu()
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    Jeu().run()