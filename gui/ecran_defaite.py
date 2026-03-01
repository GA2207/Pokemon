"""
gui/ecran_defaite.py - Ecran de defaite (Pygame).
"""

import pygame

from navigation import Ecran
from gui.composants import Bouton
from config import (WINDOW_WIDTH, WINDOW_HEIGHT, COULEUR_FOND, COULEUR_TEXTE,
                    COULEUR_TEXTE_GRIS, COULEUR_ROUGE, COULEUR_GRIS)


class EcranDefaite:
    """Ecran affiche apres une defaite."""

    def __init__(self, navigation, donnees):
        self.navigation = navigation
        self.donnees = donnees

        self.btn_retour = Bouton(WINDOW_WIDTH // 2 - 100, 450, 200, 50,
                                 "Retour au menu", COULEUR_GRIS, taille_police=18)

    def handle_event(self, event):
        if self.btn_retour.handle_event(event):
            self.navigation.reset()

    def update(self):
        pass

    def draw(self, surface):
        surface.fill(COULEUR_FOND)

        pokemon_joueur = self.donnees["pokemon_joueur"]
        pokemon_adverse = self.donnees["pokemon_adverse"]

        # Titre
        font_titre = pygame.font.SysFont("Arial", 40, bold=True)
        txt_titre = font_titre.render("DEFAITE...", True, COULEUR_ROUGE)
        surface.blit(txt_titre, (WINDOW_WIDTH // 2 - txt_titre.get_width() // 2, 120))

        # Message
        font_msg = pygame.font.SysFont("Arial", 20)
        msg = f"{pokemon_joueur.nom} a ete vaincu par {pokemon_adverse.nom}..."
        txt_msg = font_msg.render(msg, True, COULEUR_TEXTE)
        surface.blit(txt_msg, (WINDOW_WIDTH // 2 - txt_msg.get_width() // 2, 220))

        # Encouragement
        font_sub = pygame.font.SysFont("Arial", 15)
        sub = font_sub.render("Ne vous decouragez pas, retentez votre chance !",
                              True, COULEUR_TEXTE_GRIS)
        surface.blit(sub, (WINDOW_WIDTH // 2 - sub.get_width() // 2, 280))

        # Bouton
        self.btn_retour.draw(surface)
