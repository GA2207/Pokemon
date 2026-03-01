"""
config.py - Configuration globale du projet Pokemon.
Dev 4 - Chemins, constantes et parametres de l'application.
"""

import os

# ─── Chemins ──────────────────────────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
SPRITES_DIR = os.path.join(ASSETS_DIR, "sprites")

# ─── Constantes de l'application ──────────────────────────────────────────────

WINDOW_TITLE = "Pokemon - Projet Python"
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
FPS = 60

NIVEAU_DEPART = 5
POKEMON_TOTAL = 1025

# ─── Couleurs ─────────────────────────────────────────────────────────────────

COULEUR_FOND = (26, 26, 46)
COULEUR_FOND_CLAIR = (45, 45, 45)
COULEUR_FOND_CARTE = (58, 58, 58)
COULEUR_TEXTE = (255, 255, 255)
COULEUR_TEXTE_GRIS = (170, 170, 170)
COULEUR_TITRE = (255, 203, 5)
COULEUR_BLEU = (69, 123, 157)
COULEUR_ROUGE = (230, 57, 70)
COULEUR_VERT = (42, 157, 143)
COULEUR_GRIS = (108, 117, 125)
COULEUR_BLEU_CLAIR = (136, 170, 255)
