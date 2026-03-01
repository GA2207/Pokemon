"""
Tests Dev 2 adaptes pour l'integration.
Verifie TypeChart (classmethod), navigation, barre_vie, sprites.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from type_chart import TypeChart, TYPE_COLORS, TYPE_NAMES, TYPE_CHART


def test_separator(nom):
    print(f"\n{'='*50}")
    print(f"  {nom}")
    print(f"{'='*50}")


# ─── Tests TypeChart ──────────────────────────────────────────────────────────
test_separator("TESTS TYPE_CHART (Dev 2 adaptes)")

# Constantes exportees
assert len(TYPE_NAMES) == 18, f"Attendu 18 types, got {len(TYPE_NAMES)}"
assert "Feu" in TYPE_NAMES
assert "Eau" in TYPE_NAMES
print("[OK] TYPE_NAMES exporte avec 18 types")

assert len(TYPE_COLORS) == 18
assert TYPE_COLORS["Feu"]["hex"] == "#F08030"
assert TYPE_COLORS["Eau"]["rgb"] == (104, 144, 240)
print("[OK] TYPE_COLORS exporte avec hex et rgb")

assert len(TYPE_CHART) == 18
assert len(TYPE_CHART[0]) == 18
print("[OK] TYPE_CHART exporte (matrice 18x18)")

# Classmethod
assert TypeChart.get_efficacite("Feu", "Plante") == 2
assert TypeChart.get_efficacite("Eau", "Feu") == 2
assert TypeChart.get_efficacite("Electrik", "Sol") == 0
print("[OK] TypeChart.get_efficacite (classmethod)")

assert TypeChart.get_multiplicateur("Electrik", ["Eau", "Vol"]) == 4
print("[OK] TypeChart.get_multiplicateur double type")

faiblesses = TypeChart.get_faiblesses("Feu")
assert "Eau" in faiblesses
assert "Roche" in faiblesses
print("[OK] TypeChart.get_faiblesses")

immunites = TypeChart.get_immunites("Spectre")
assert "Normal" in immunites
print("[OK] TypeChart.get_immunites")

assert TypeChart.est_type_valide("Feu") == True
assert TypeChart.est_type_valide("Lave") == False
print("[OK] TypeChart.est_type_valide")

assert TypeChart.get_message_efficacite(2) == "C'est super efficace !"
assert TypeChart.get_message_efficacite(0) == "Ca n'affecte pas le Pokemon..."
print("[OK] Messages efficacite")


# ─── Tests Navigation ─────────────────────────────────────────────────────────
test_separator("TESTS NAVIGATION (Dev 2)")

from navigation import Navigation, Ecran

nav = Navigation()
assert nav.get_ecran_actuel() == Ecran.MENU_PRINCIPAL
print("[OK] Ecran initial = MENU_PRINCIPAL")

nav.aller_a(Ecran.SELECTION_POKEMON)
assert nav.get_ecran_actuel() == Ecran.SELECTION_POKEMON
print("[OK] Navigation vers SELECTION_POKEMON")

nav.aller_a(Ecran.COMBAT, {"pokemon": "Pikachu"})
assert nav.get_ecran_actuel() == Ecran.COMBAT
assert nav.get_donnees_actuelles()["pokemon"] == "Pikachu"
print("[OK] Navigation avec donnees")

nav.retour()
assert nav.get_ecran_actuel() == Ecran.SELECTION_POKEMON
print("[OK] Retour arriere")

assert nav.peut_revenir() == True
nav.reset()
assert nav.get_ecran_actuel() == Ecran.MENU_PRINCIPAL
assert nav.peut_revenir() == False
print("[OK] Reset navigation")


# ─── Tests BarreVie ───────────────────────────────────────────────────────────
test_separator("TESTS BARRE_VIE (Dev 2)")

from barre_vie import BarreVie, BarreVieDouble

bv = BarreVie(100, 100, "Pikachu")
assert bv.get_pourcentage() == 1.0
assert bv.get_couleur_hex() == "#16A34A"  # Vert
assert bv.get_etat() == "haute"
assert bv.est_ko() == False
print("[OK] BarreVie a 100%")

bv.pv_actuel = 30
assert bv.get_etat() == "moyenne"
assert bv.get_couleur_hex() == "#EAB308"  # Jaune
print("[OK] BarreVie a 30% (jaune)")

bv.pv_actuel = 10
assert bv.get_etat() == "basse"
assert bv.get_couleur_hex() == "#DC2626"  # Rouge
print("[OK] BarreVie a 10% (rouge)")

bv.appliquer_degats(10)
assert bv.est_ko() == True
print("[OK] BarreVie KO apres degats")

# BarreVieDouble
bv1 = BarreVie(100, 80, "Joueur")
bv2 = BarreVie(120, 60, "Adverse")
bvd = BarreVieDouble(bv1, bv2)
donnees = bvd.get_donnees_gui()
assert "joueur" in donnees
assert "adverse" in donnees
print("[OK] BarreVieDouble GUI data")


# ─── Tests Sprites ────────────────────────────────────────────────────────────
test_separator("TESTS SPRITES (Dev 2)")

from sprites import SpriteManager

sm = SpriteManager(mode_gui="terminal")
sprite = sm.get_sprite_ascii("025")
assert isinstance(sprite, list)
assert len(sprite) > 0
print("[OK] Sprite ASCII Pikachu")

sprite_defaut = sm.get_sprite_ascii("999")
assert isinstance(sprite_defaut, list)
print("[OK] Sprite par defaut pour numero inconnu")

badge = sm.get_badge_type("Feu")
assert badge["nom"] == "Feu"
assert badge["hex"] == "#F08030"
print("[OK] Badge type avec couleur")


# ─── Resume ───────────────────────────────────────────────────────────────────
print(f"\n{'='*50}")
print("  TOUS LES TESTS DEV 2 SONT PASSES !")
print(f"{'='*50}")
