"""
gui/ecran_victoire.py - Ecran de victoire (Pygame).
"""

import pygame

from navigation import Ecran
from experience import Experience
from gui.composants import Bouton
from config import (WINDOW_WIDTH, WINDOW_HEIGHT, COULEUR_FOND, COULEUR_TEXTE,
                    COULEUR_TITRE, COULEUR_VERT, COULEUR_BLEU, COULEUR_FOND_CLAIR)


class EcranVictoire:
    """Ecran affiche apres une victoire ou capture reussie."""

    def __init__(self, navigation, donnees):
        self.navigation = navigation
        self.donnees = donnees

        self.btn_retour = Bouton(WINDOW_WIDTH // 2 - 100, 550, 200, 50,
                                 "Retour au menu", COULEUR_BLEU, taille_police=18)

    def handle_event(self, event):
        if self.btn_retour.handle_event(event):
            self.navigation.reset()

    def update(self):
        pass

    def draw(self, surface):
        surface.fill(COULEUR_FOND)

        pokemon_joueur = self.donnees["pokemon_joueur"]
        pokemon_adverse = self.donnees["pokemon_adverse"]
        combat = self.donnees.get("combat")

        if combat and combat.capture_reussie:
            titre = "CAPTURE REUSSIE !"
            couleur_titre = COULEUR_VERT
            message = f"Vous avez capture {pokemon_adverse.nom} !"
        else:
            titre = "VICTOIRE !"
            couleur_titre = COULEUR_TITRE
            message = f"{pokemon_joueur.nom} a vaincu {pokemon_adverse.nom} !"

        # Titre
        font_titre = pygame.font.SysFont("Arial", 40, bold=True)
        txt_titre = font_titre.render(titre, True, couleur_titre)
        surface.blit(txt_titre, (WINDOW_WIDTH // 2 - txt_titre.get_width() // 2, 80))

        # Message
        font_msg = pygame.font.SysFont("Arial", 20)
        txt_msg = font_msg.render(message, True, COULEUR_TEXTE)
        surface.blit(txt_msg, (WINDOW_WIDTH // 2 - txt_msg.get_width() // 2, 160))

        # Resume
        pygame.draw.rect(surface, COULEUR_FOND_CLAIR,
                         (WINDOW_WIDTH // 2 - 250, 220, 500, 160), border_radius=8)

        pct = Experience.pourcentage_niveau(pokemon_joueur.xp, pokemon_joueur.niveau)
        xp_reste = Experience.xp_restante_pour_prochain_niveau(
            pokemon_joueur.xp, pokemon_joueur.niveau)

        font_info = pygame.font.SysFont("Arial", 16)
        infos = [
            f"{pokemon_joueur.nom} - Niveau {pokemon_joueur.niveau}",
            f"PV : {pokemon_joueur.pv}/{pokemon_joueur.pv_max}",
            f"XP : {pct}% vers le prochain niveau ({xp_reste} XP restante)",
        ]

        for i, info in enumerate(infos):
            txt = font_info.render(info, True, COULEUR_TEXTE)
            surface.blit(txt, (WINDOW_WIDTH // 2 - 230, 240 + i * 35))

        # Bouton
        self.btn_retour.draw(surface)
