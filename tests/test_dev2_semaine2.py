"""
Tests Dev 2 semaine 2 adaptes pour l'integration.
Verifie ecran_pokedex, navigation avancee, barre_vie avancee.
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pokedex import Pokedex
from pokemon import Pokemon
from ecran_pokedex import EcranPokedex
from navigation import Navigation, Ecran
from barre_vie import BarreVie


def test_separator(nom):
    print(f"\n{'='*50}")
    print(f"  {nom}")
    print(f"{'='*50}")


# ─── Tests EcranPokedex ──────────────────────────────────────────────────────
test_separator("TESTS ECRAN_POKEDEX (Dev 2 Semaine 2)")

# Creer un Pokedex avec des donnees
pokedex = Pokedex(chemin_json=tempfile.mktemp(suffix=".json"))

donnees_pokemon = [
    {"numero": 4, "nom": "Salameche", "types": ["Feu"], "pv": 39,
     "attaque": 52, "defense": 43, "attaque_speciale": 60,
     "defense_speciale": 50, "vitesse": 65, "base_xp": 62, "taux_capture": 45},
    {"numero": 7, "nom": "Carapuce", "types": ["Eau"], "pv": 44,
     "attaque": 48, "defense": 65, "attaque_speciale": 50,
     "defense_speciale": 64, "vitesse": 43, "base_xp": 63, "taux_capture": 45},
    {"numero": 25, "nom": "Pikachu", "types": ["Electrik"], "pv": 35,
     "attaque": 55, "defense": 40, "attaque_speciale": 50,
     "defense_speciale": 50, "vitesse": 90, "base_xp": 112, "taux_capture": 190},
]

for d in donnees_pokemon:
    p = Pokemon.depuis_json(d, niveau=5)
    pokedex.enregistrer_capture(p)

ecran = EcranPokedex(pokedex)

# Test compteur
assert pokedex.get_nombre() == f"3/{Pokedex.TOTAL_POKEMON}"
print(f"[OK] Compteur Pokedex = {pokedex.get_nombre()}")

# Test liste
pokemons = pokedex._pokemons
assert len(pokemons) == 3
print(f"[OK] {len(pokemons)} Pokemon dans la liste")

# Test recherche
result = pokedex.rechercher("pikachu")
assert result is not None
assert result["nom"] == "Pikachu"
print("[OK] Recherche par nom (insensible casse)")

result_none = pokedex.rechercher("Mewtwo")
assert result_none is None
print("[OK] Recherche nom inexistant = None")

# Test donnees GUI
donnees_gui = ecran.get_donnees_gui()
assert "compteur" in donnees_gui
assert "liste_filtree" in donnees_gui
assert "couleurs_types" in donnees_gui
assert donnees_gui["total"] == Pokedex.TOTAL_POKEMON
print("[OK] Donnees GUI ecran Pokedex")


# ─── Tests Navigation avancee ─────────────────────────────────────────────────
test_separator("TESTS NAVIGATION AVANCEE")

nav = Navigation()

# Test remplacer
nav.aller_a(Ecran.SELECTION_POKEMON)
nav.remplacer(Ecran.COMBAT)
assert nav.get_ecran_actuel() == Ecran.COMBAT
historique = nav.get_historique()
assert len(historique) == 2  # MENU + COMBAT (SELECTION remplace)
print("[OK] Navigation remplacer")

# Test est_sur
assert nav.est_sur(Ecran.COMBAT) == True
assert nav.est_sur(Ecran.MENU_PRINCIPAL) == False
print("[OK] Navigation est_sur")

# Test callback
callback_appele = [False]
def mon_callback(ecran, donnees):
    callback_appele[0] = True

nav.enregistrer_callback(Ecran.POKEDEX, mon_callback)
nav.aller_a(Ecran.POKEDEX)
assert callback_appele[0] == True
print("[OK] Callback ecran specifique")


# ─── Tests BarreVie avances ──────────────────────────────────────────────────
test_separator("TESTS BARRE_VIE AVANCES")

bv = BarreVie(200, 200, "Dracaufeu")

# Test soigner
bv.appliquer_degats(100)
assert bv.pv_actuel == 100
bv.soigner(50)
assert bv.pv_actuel == 150
print("[OK] Soigner apres degats")

# Test soigner au-dela du max
bv.soigner(999)
assert bv.pv_actuel == 200
print("[OK] Soin plafonne a pv_max")

# Test reinitialiser
bv.appliquer_degats(150)
bv.reinitialiser()
assert bv.pv_actuel == 200
print("[OK] Reinitialiser PV")

# Test donnees GUI
donnees = bv.get_donnees_gui()
assert donnees["nom"] == "Dracaufeu"
assert donnees["pv_max"] == 200
assert donnees["pourcentage"] == 1.0
assert donnees["couleur_hex"] == "#16A34A"
print("[OK] Donnees GUI barre vie")


# ─── Resume ───────────────────────────────────────────────────────────────────
print(f"\n{'='*50}")
print("  TOUS LES TESTS DEV 2 SEMAINE 2 SONT PASSES !")
print(f"{'='*50}")
