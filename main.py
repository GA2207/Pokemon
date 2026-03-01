"""
main.py - Point d'entree de l'application Pokemon.
Dev 1 - Lance la fenetre Pygame et charge les donnees.
"""

import os
import sys

# Ajouter le dossier courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pygame

from config import WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from pokemon import Pokemon
from inventaire import Inventaire
from pokedex import Pokedex
from gui.app import App


def main():
    # Charger les donnees
    print("Chargement des Pokemon...")
    tous_les_pokemon = Pokemon.charger_tous()
    print(f"{len(tous_les_pokemon)} Pokemon charges.")

    # Creer l'inventaire de depart
    inventaire = Inventaire()
    inventaire.creer_inventaire_depart()

    # Creer ou charger le Pokedex
    pokedex = Pokedex()
    pokedex.charger()

    # Initialiser Pygame
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()

    # Lancer l'application
    app = App(screen, tous_les_pokemon, inventaire, pokedex)

    # Boucle principale
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                app.handle_event(event)

        app.update()
        app.draw()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
