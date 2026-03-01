"""
utils.py - Fonctions utilitaires pour le projet Pokemon.
Dev 4
"""

import random

from pokemon import Pokemon


def numero_to_str(numero):
    """Convertit un numero en chaine formatee sur 3 chiffres (ex: 25 -> '025')."""
    return str(numero).zfill(3)


def charger_pokemon_aleatoire(tous_les_pokemon, niveau=None):
    """
    Charge un Pokemon aleatoire depuis la liste complete.

    Args:
        tous_les_pokemon (list): Liste de dicts issus de pokemon.json.
        niveau (int, optional): Niveau du Pokemon. Aleatoire si None.

    Returns:
        Pokemon: Instance de Pokemon.
    """
    donnees = random.choice(tous_les_pokemon)
    niv = niveau if niveau else random.randint(3, 15)
    return Pokemon.depuis_json(donnees, niveau=niv)
