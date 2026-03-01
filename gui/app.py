"""
gui/app.py - Controleur principal de l'application Pygame.
Gere le swap d'ecrans selon la navigation.
"""

import pygame

from navigation import Navigation, Ecran
from gui.ecran_menu import EcranMenu
from gui.ecran_selection import EcranSelection
from gui.ecran_combat import EcranCombatGUI
from gui.ecran_pokedex_gui import EcranPokedexGUI
from gui.ecran_victoire import EcranVictoire
from gui.ecran_defaite import EcranDefaite
from gui.ecran_ajout import EcranAjout


class App:
    """Controleur principal : gere la boucle Pygame et le swap d'ecrans."""

    def __init__(self, screen, tous_les_pokemon, inventaire, pokedex):
        self.screen = screen
        self.tous_les_pokemon = tous_les_pokemon
        self.inventaire = inventaire
        self.pokedex = pokedex

        self.navigation = Navigation()
        self.navigation.enregistrer_callback_global(self._on_changement_ecran)

        self._ecran_actuel = None
        self._afficher_ecran(Ecran.MENU_PRINCIPAL, {})

    def _on_changement_ecran(self, ecran, donnees):
        """Callback appele a chaque changement d'ecran."""
        self._afficher_ecran(ecran, donnees)

    def _afficher_ecran(self, ecran, donnees):
        """Cree le nouvel ecran."""
        self._ecran_actuel = self._creer_ecran(ecran, donnees)

    def _creer_ecran(self, ecran, donnees):
        """Cree l'ecran correspondant."""
        if ecran == Ecran.MENU_PRINCIPAL:
            return EcranMenu(self.navigation, self.pokedex)

        elif ecran == Ecran.SELECTION_POKEMON:
            return EcranSelection(
                self.navigation, self.tous_les_pokemon,
                self.inventaire, self.pokedex
            )

        elif ecran == Ecran.COMBAT:
            return EcranCombatGUI(
                self.navigation, donnees,
                self.inventaire, self.pokedex
            )

        elif ecran == Ecran.POKEDEX:
            return EcranPokedexGUI(self.navigation, self.pokedex)

        elif ecran == Ecran.VICTOIRE:
            return EcranVictoire(self.navigation, donnees)

        elif ecran == Ecran.DEFAITE:
            return EcranDefaite(self.navigation, donnees)

        elif ecran == Ecran.AJOUTER_POKEMON:
            return EcranAjout(
                self.navigation, self.tous_les_pokemon, self.pokedex
            )

        return None

    def handle_event(self, event):
        """Delegue les events a l'ecran actuel."""
        if self._ecran_actuel:
            self._ecran_actuel.handle_event(event)

    def update(self):
        """Met a jour l'ecran actuel."""
        if self._ecran_actuel:
            self._ecran_actuel.update()

    def draw(self):
        """Dessine l'ecran actuel."""
        if self._ecran_actuel:
            self._ecran_actuel.draw(self.screen)
