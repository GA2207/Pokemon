"""
gui/ecran_pokedex_gui.py - Ecran Pokedex (Pygame).
"""

import pygame

from navigation import Ecran
from type_chart import TYPE_COLORS, TYPE_NAMES
from pokedex import Pokedex
from gui.composants import Bouton, ListeScrollable, dessiner_badge_type
from config import (WINDOW_WIDTH, WINDOW_HEIGHT, COULEUR_FOND, COULEUR_TEXTE,
                    COULEUR_TEXTE_GRIS, COULEUR_TITRE, COULEUR_GRIS,
                    COULEUR_BLEU_CLAIR, COULEUR_FOND_CLAIR)


class EcranPokedexGUI:
    """Ecran Pokedex : filtres par type, liste, detail, compteur."""

    def __init__(self, navigation, pokedex):
        self.navigation = navigation
        self.pokedex = pokedex
        self._filtre = None

        # Liste
        self.liste = ListeScrollable(20, 100, WINDOW_WIDTH - 40, 380)
        self._entries_filtrees = []
        self._remplir_liste()

        # Boutons filtres type
        self.btn_filtres = []
        x = 20
        # Bouton "Tous"
        self.btn_tous = Bouton(x, 60, 45, 26, "Tous", (85, 85, 85), taille_police=11)
        x += 50
        for type_nom in TYPE_NAMES:
            couleur = TYPE_COLORS.get(type_nom, {}).get("rgb", (136, 136, 136))
            btn = Bouton(x, 60, 45, 26, type_nom[:3], couleur, taille_police=10)
            self.btn_filtres.append((type_nom, btn))
            x += 48

        # Bouton retour
        self.btn_retour = Bouton(20, 640, 140, 40, "Retour", COULEUR_GRIS)

        # Detail
        self._detail_texte = "Selectionnez un Pokemon"

    def _get_entries(self):
        entries = []
        for numero, entry in sorted(self.pokedex._entries.items()):
            if self._filtre and self._filtre not in entry["types"]:
                continue
            entries.append((numero, entry))
        return entries

    def _remplir_liste(self):
        self._entries_filtrees = self._get_entries()
        items = []
        if not self._entries_filtrees:
            items.append("  Aucun Pokemon dans votre Pokedex.")
        else:
            for numero, entry in self._entries_filtrees:
                types_str = "/".join(entry["types"])
                icon = "O" if entry["statut"] == "capture" else "-"
                items.append(f" [{icon}] #{numero:04d}  {entry['nom']:<16} {types_str}")
        self.liste.set_items(items)

    def handle_event(self, event):
        if self.btn_retour.handle_event(event):
            self.navigation.retour()
            return

        if self.btn_tous.handle_event(event):
            self._filtre = None
            self._remplir_liste()
            return

        for type_nom, btn in self.btn_filtres:
            if btn.handle_event(event):
                self._filtre = type_nom
                self._remplir_liste()
                return

        if self.liste.handle_event(event):
            idx = self.liste.get_selection()
            if 0 <= idx < len(self._entries_filtrees):
                numero, entry = self._entries_filtrees[idx]
                types_str = " / ".join(entry["types"])
                statut = "Capture" if entry["statut"] == "capture" else "Vu"
                self._detail_texte = (
                    f"#{numero:04d}  {entry['nom']}  |  Types: {types_str}  |  "
                    f"Statut: {statut}"
                )
                if entry["statut"] == "capture":
                    self._detail_texte += (
                        f"  |  PV:{entry.get('pv','?')} ATK:{entry.get('attaque','?')} "
                        f"DEF:{entry.get('defense','?')} VIT:{entry.get('vitesse','?')}"
                    )

    def update(self):
        pass

    def draw(self, surface):
        surface.fill(COULEUR_FOND)

        # En-tete
        font_titre = pygame.font.SysFont("Arial", 28, bold=True)
        titre = font_titre.render("POKEDEX", True, COULEUR_TITRE)
        surface.blit(titre, (20, 12))

        stats = self.pokedex.get_stats()
        font_stats = pygame.font.SysFont("Arial", 14)
        txt = font_stats.render(
            f"Vus: {stats['vus']}/{Pokedex.TOTAL_POKEMON}  |  "
            f"Captures: {stats['captures']}/{Pokedex.TOTAL_POKEMON}",
            True, COULEUR_BLEU_CLAIR)
        surface.blit(txt, (WINDOW_WIDTH - txt.get_width() - 20, 22))

        # Filtres label
        font_lbl = pygame.font.SysFont("Arial", 12)
        lbl = font_lbl.render("Filtrer :", True, COULEUR_TEXTE)
        surface.blit(lbl, (20, 46))

        # Boutons filtres
        self.btn_tous.draw(surface)
        for _, btn in self.btn_filtres:
            btn.draw(surface)

        # Liste
        self.liste.draw(surface)

        # Detail
        font_detail = pygame.font.SysFont("Arial", 13)
        pygame.draw.rect(surface, COULEUR_FOND_CLAIR,
                         (20, 490, WINDOW_WIDTH - 40, 60), border_radius=6)
        detail_lines = self._detail_texte.split("|")
        for i, line in enumerate(detail_lines):
            txt = font_detail.render(line.strip(), True, COULEUR_TEXTE)
            surface.blit(txt, (30, 498 + i * 18))

        # Compteur
        font_count = pygame.font.SysFont("Arial", 13)
        nb = len(self._entries_filtrees)
        filtre_txt = f"  (type: {self._filtre})" if self._filtre else ""
        count = font_count.render(f"{nb} Pokemon{filtre_txt}", True, COULEUR_TEXTE_GRIS)
        surface.blit(count, (20, 570))

        # Bouton retour
        self.btn_retour.draw(surface)
