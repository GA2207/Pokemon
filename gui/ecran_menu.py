"""
gui/ecran_menu.py - Menu principal du jeu Pokemon (Pygame).
"""

import pygame
from navigation import Ecran
from gui.composants import Bouton
from config import (WINDOW_WIDTH, WINDOW_HEIGHT, COULEUR_FOND, COULEUR_TEXTE,
                    COULEUR_TITRE, COULEUR_ROUGE, COULEUR_BLEU, COULEUR_VERT,
                    COULEUR_GRIS, COULEUR_BLEU_CLAIR)


class EcranMenu:
    """Menu principal avec 4 boutons."""

    def __init__(self, navigation, pokedex):
        self.navigation = navigation
        self.pokedex = pokedex

        cx = WINDOW_WIDTH // 2
        bw, bh = 280, 50

        self.boutons = [
            ("combat", Bouton(cx - bw // 2, 300, bw, bh, "Combat", COULEUR_ROUGE, taille_police=18)),
            ("ajouter", Bouton(cx - bw // 2, 365, bw, bh, "Ajouter Pokemon", COULEUR_BLEU, taille_police=18)),
            ("pokedex", Bouton(cx - bw // 2, 430, bw, bh, "Pokedex", COULEUR_VERT, taille_police=18)),
            ("quitter", Bouton(cx - bw // 2, 495, bw, bh, "Quitter", COULEUR_GRIS, taille_police=18)),
        ]

    def handle_event(self, event):
        for nom, btn in self.boutons:
            if btn.handle_event(event):
                if nom == "combat":
                    self.navigation.aller_a(Ecran.SELECTION_POKEMON)
                elif nom == "ajouter":
                    self.navigation.aller_a(Ecran.AJOUTER_POKEMON)
                elif nom == "pokedex":
                    self.navigation.aller_a(Ecran.POKEDEX)
                elif nom == "quitter":
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

    def update(self):
        pass

    def draw(self, surface):
        surface.fill(COULEUR_FOND)

        # Titre
        font_titre = pygame.font.SysFont("Arial", 48, bold=True)
        titre = font_titre.render("POKEMON", True, COULEUR_TITRE)
        surface.blit(titre, (WINDOW_WIDTH // 2 - titre.get_width() // 2, 80))

        # Sous-titre
        font_sub = pygame.font.SysFont("Arial", 18)
        sub = font_sub.render("Projet Python", True, (170, 170, 170))
        surface.blit(sub, (WINDOW_WIDTH // 2 - sub.get_width() // 2, 145))

        # Stats Pokedex
        stats = self.pokedex.get_stats()
        font_stats = pygame.font.SysFont("Arial", 14)
        txt_stats = font_stats.render(
            f"Pokedex : {stats['vus']} vus / {stats['captures']} captures",
            True, COULEUR_BLEU_CLAIR)
        surface.blit(txt_stats, (WINDOW_WIDTH // 2 - txt_stats.get_width() // 2, 200))

        # Boutons
        for _, btn in self.boutons:
            btn.draw(surface)
