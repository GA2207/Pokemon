"""
Tests d'integration - Parcours complet du jeu.
Selection -> Combat -> Capture -> Pokedex
"""

import os
import sys
import tempfile
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pokemon import Pokemon
from combat import Combat
from inventaire import Inventaire, POKE_BALL, MASTER_BALL
from pokedex import Pokedex
from type_chart import TypeChart, TYPE_COLORS, TYPE_NAMES
from experience import Experience
from navigation import Navigation, Ecran
from barre_vie import BarreVie
from sprites import SpriteManager
from config import WINDOW_WIDTH, WINDOW_HEIGHT, POKEMON_TOTAL, NIVEAU_DEPART
from utils import numero_to_str, charger_pokemon_aleatoire


def test_separator(nom):
    print(f"\n{'='*50}")
    print(f"  {nom}")
    print(f"{'='*50}")


# ─── Test 1 : Chargement des donnees ─────────────────────────────────────────
test_separator("TEST 1 : CHARGEMENT DES DONNEES")

tous_les_pokemon = Pokemon.charger_tous()
assert len(tous_les_pokemon) == 1025, f"Attendu 1025, got {len(tous_les_pokemon)}"
print(f"[OK] {len(tous_les_pokemon)} Pokemon charges")

# Config
assert POKEMON_TOTAL == 1025
assert WINDOW_WIDTH == 900
assert NIVEAU_DEPART == 5
print("[OK] Config chargee")

# Utils
assert numero_to_str(25) == "025"
assert numero_to_str(1) == "001"
print("[OK] numero_to_str")

poke_random = charger_pokemon_aleatoire(tous_les_pokemon, niveau=10)
assert poke_random.niveau == 10
assert poke_random.pv > 0
print(f"[OK] Pokemon aleatoire : {poke_random.nom} (Niv.{poke_random.niveau})")


# ─── Test 2 : Selection et creation Pokemon ───────────────────────────────────
test_separator("TEST 2 : SELECTION POKEMON")

donnees_joueur = tous_les_pokemon[24]  # Pikachu
pokemon_joueur = Pokemon.depuis_json(donnees_joueur, niveau=NIVEAU_DEPART)
assert pokemon_joueur.nom == "Pikachu"
assert pokemon_joueur.niveau == NIVEAU_DEPART
print(f"[OK] Joueur : {pokemon_joueur.nom} Niv.{pokemon_joueur.niveau}")

donnees_adverse = tous_les_pokemon[3]  # Index 3 = numero 4
pokemon_adverse = Pokemon.depuis_json(donnees_adverse, niveau=NIVEAU_DEPART + 2)
assert pokemon_adverse.numero == 4
print(f"[OK] Adverse : {pokemon_adverse.nom} Niv.{pokemon_adverse.niveau}")


# ─── Test 3 : Combat complet ─────────────────────────────────────────────────
test_separator("TEST 3 : COMBAT COMPLET")

inventaire = Inventaire()
inventaire.creer_inventaire_depart()

pokedex = Pokedex(chemin_json=tempfile.mktemp(suffix=".json"))

combat = Combat(pokemon_joueur, pokemon_adverse, inventaire, pokedex)

# L'adverse doit etre enregistre comme vu
assert pokedex.est_vu(pokemon_adverse.numero)
print("[OK] Adverse enregistre comme vu dans le Pokedex")

# Jouer quelques tours
for i in range(3):
    if combat.termine:
        break
    msgs = combat.tour_attaque()
    assert len(msgs) > 0

print(f"[OK] {combat.tour} tours joues")

# Etat du combat
etat = combat.get_etat()
assert "joueur" in etat
assert "adverse" in etat
assert etat["joueur"]["nom"] == "Pikachu"
print("[OK] Etat du combat correct")


# ─── Test 4 : Capture avec Master Ball ────────────────────────────────────────
test_separator("TEST 4 : CAPTURE")

# Nouveau combat pour tester la capture
joueur2 = Pokemon.depuis_json(donnees_joueur, niveau=20)
adverse2 = Pokemon.depuis_json(donnees_adverse, niveau=5)
inv2 = Inventaire()
inv2.ajouter(MASTER_BALL, 1)
pokedex2 = Pokedex(chemin_json=tempfile.mktemp(suffix=".json"))

combat2 = Combat(joueur2, adverse2, inv2, pokedex2)

msgs = combat2.tenter_capture(MASTER_BALL)
assert combat2.capture_reussie == True
assert combat2.termine == True
assert pokedex2.est_capture(adverse2.numero)
print(f"[OK] {adverse2.nom} capture avec Master Ball")

# Pokedex stats
stats = pokedex2.get_stats()
assert stats["captures"] == 1
print(f"[OK] Pokedex : {stats['captures']} capture(s)")


# ─── Test 5 : Pokedex compatibilite ──────────────────────────────────────────
test_separator("TEST 5 : POKEDEX COMPATIBILITE DEV 2")

# Test propriete _pokemons
pokemons_liste = pokedex2._pokemons
assert isinstance(pokemons_liste, list)
assert len(pokemons_liste) == 1
assert "numero" in pokemons_liste[0]
assert "nom" in pokemons_liste[0]
print("[OK] _pokemons retourne une liste de dicts")

# Test rechercher
result = pokedex2.rechercher(pokemon_adverse.nom)
assert result is not None
assert result["nom"] == pokemon_adverse.nom
print("[OK] rechercher() par nom insensible a la casse")

# Test get_nombre
nombre = pokedex2.get_nombre()
assert nombre == "1/1025"
print(f"[OK] get_nombre() = {nombre}")

# Test get_nombre_int
assert pokedex2.get_nombre_int() == 1
print("[OK] get_nombre_int() = 1")


# ─── Test 6 : Navigation ─────────────────────────────────────────────────────
test_separator("TEST 6 : NAVIGATION")

nav = Navigation()
assert nav.get_ecran_actuel() == Ecran.MENU_PRINCIPAL

nav.aller_a(Ecran.SELECTION_POKEMON)
nav.aller_a(Ecran.COMBAT, {"pokemon": pokemon_joueur})
assert nav.get_ecran_actuel() == Ecran.COMBAT

nav.retour()
assert nav.get_ecran_actuel() == Ecran.SELECTION_POKEMON

nav.reset()
assert nav.get_ecran_actuel() == Ecran.MENU_PRINCIPAL
print("[OK] Navigation complete : aller, retour, reset")


# ─── Test 7 : Barres de vie et sprites ────────────────────────────────────────
test_separator("TEST 7 : BARRE VIE & SPRITES")

bv = BarreVie(100, 75, "Test")
assert bv.get_pourcentage() == 0.75
assert bv.get_etat() == "haute"
print("[OK] BarreVie calculs")

sm = SpriteManager(mode_gui="terminal")
sprite = sm.get_sprite_ascii("025")
assert len(sprite) > 0
badge = sm.get_badge_type("Electrik")
assert badge["hex"] == "#F8D030"
print("[OK] SpriteManager ASCII + badges")


# ─── Test 8 : Types et couleurs ──────────────────────────────────────────────
test_separator("TEST 8 : TYPES & COULEURS")

assert len(TYPE_NAMES) == 18
assert len(TYPE_COLORS) == 18
for type_nom in TYPE_NAMES:
    assert type_nom in TYPE_COLORS, f"{type_nom} manquant dans TYPE_COLORS"
    assert "hex" in TYPE_COLORS[type_nom]
    assert "rgb" in TYPE_COLORS[type_nom]
print("[OK] 18 types avec couleurs hex + rgb")


# ─── Resume ───────────────────────────────────────────────────────────────────
print(f"\n{'='*50}")
print("  TOUS LES TESTS D'INTEGRATION SONT PASSES !")
print(f"{'='*50}")
