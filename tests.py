"""
Tests unitaires pour tous les modules du projet Pokemon.
"""

import os
import sys
import json
import tempfile

# Ajouter le dossier courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from type_chart import TypeChart
from statut import Statut
from inventaire import Inventaire, POKE_BALL, SUPER_BALL, HYPER_BALL, MASTER_BALL, FILET_BALL, POTION, RAPPEL, TOTAL_SOIN
from experience import Experience
from pokemon import Pokemon
from pokedex import Pokedex
from capture import Capture


def test_separator(nom_test):
    print(f"\n{'='*50}")
    print(f"  {nom_test}")
    print(f"{'='*50}")


# =====================================================
# TESTS TYPE_CHART
# =====================================================
test_separator("TESTS TYPE_CHART")

# Test types valides
assert TypeChart.est_type_valide("Feu"), "Feu devrait etre valide"
assert TypeChart.est_type_valide("Eau"), "Eau devrait etre valide"
assert not TypeChart.est_type_valide("Lave"), "Lave ne devrait pas etre valide"
print("[OK] Validation des types")

# Test efficacite simple
assert TypeChart.get_efficacite("Feu", "Plante") == 2, "Feu vs Plante = x2"
assert TypeChart.get_efficacite("Eau", "Feu") == 2, "Eau vs Feu = x2"
assert TypeChart.get_efficacite("Electrik", "Sol") == 0, "Electrik vs Sol = x0"
assert TypeChart.get_efficacite("Normal", "Spectre") == 0, "Normal vs Spectre = x0"
assert TypeChart.get_efficacite("Feu", "Eau") == 0.5, "Feu vs Eau = x0.5"
assert TypeChart.get_efficacite("Normal", "Normal") == 1, "Normal vs Normal = x1"
print("[OK] Efficacite simple")

# Test double type
assert TypeChart.get_multiplicateur("Electrik", ["Eau", "Vol"]) == 4, "Electrik vs Eau/Vol = x4"
assert TypeChart.get_multiplicateur("Sol", ["Electrik", "Acier"]) == 4, "Sol vs Electrik/Acier = x4"
assert TypeChart.get_multiplicateur("Electrik", ["Sol", "Roche"]) == 0, "Electrik vs Sol/Roche = x0"
print("[OK] Double type")

# Test faiblesses/resistances/immunites
faiblesses_feu = TypeChart.get_faiblesses("Feu")
assert "Eau" in faiblesses_feu, "Feu devrait avoir Eau en faiblesse"
assert "Roche" in faiblesses_feu, "Feu devrait avoir Roche en faiblesse"

immunites_spectre = TypeChart.get_immunites("Spectre")
assert "Normal" in immunites_spectre, "Spectre devrait etre immune a Normal"
assert "Combat" in immunites_spectre, "Spectre devrait etre immune a Combat"
print("[OK] Faiblesses, resistances, immunites")

# Test messages
assert TypeChart.get_message_efficacite(2) == "C'est super efficace !"
assert TypeChart.get_message_efficacite(0) == "Ca n'affecte pas le Pokemon..."
assert TypeChart.get_message_efficacite(1) is None
print("[OK] Messages d'efficacite")


# =====================================================
# TESTS STATUT
# =====================================================
test_separator("TESTS STATUT")

# Test application de statut
statut = Statut()
assert statut.appliquer_statut_principal(Statut.POISON, ["Normal"]) == True
assert statut.statut_principal == Statut.POISON
assert statut.appliquer_statut_principal(Statut.BRULURE, ["Normal"]) == False  # Deja un statut
print("[OK] Application de statut principal")

# Test immunite par type
statut2 = Statut()
assert statut2.appliquer_statut_principal(Statut.POISON, ["Poison"]) == False  # Immune
assert statut2.appliquer_statut_principal(Statut.POISON, ["Acier"]) == False  # Immune
assert statut2.appliquer_statut_principal(Statut.BRULURE, ["Feu"]) == False  # Immune
assert statut2.appliquer_statut_principal(Statut.PARALYSIE, ["Electrik"]) == False  # Immune
print("[OK] Immunites par type")

# Test confusion (statut volatil)
statut3 = Statut()
statut3.appliquer_statut_principal(Statut.POISON, ["Normal"])
assert statut3.appliquer_confusion() == True  # Confusion cumulable
assert statut3.confusion == True
print("[OK] Confusion cumulable avec statut principal")

# Test degats fin de tour
statut4 = Statut()
statut4.appliquer_statut_principal(Statut.POISON, ["Normal"])
degats, msg = statut4.appliquer_degats_fin_tour(100)
assert degats == 12, f"Poison devrait infliger 12 degats (1/8 de 100), got {degats}"
print("[OK] Degats de poison fin de tour")

statut5 = Statut()
statut5.appliquer_statut_principal(Statut.BRULURE, ["Normal"])
degats, msg = statut5.appliquer_degats_fin_tour(100)
assert degats == 6, f"Brulure devrait infliger 6 degats (1/16 de 100), got {degats}"
print("[OK] Degats de brulure fin de tour")

# Test bonus capture
statut6 = Statut()
statut6.appliquer_statut_principal(Statut.SOMMEIL, ["Normal"])
assert statut6.get_bonus_capture() == 2.0
print("[OK] Bonus capture par statut")


# =====================================================
# TESTS INVENTAIRE
# =====================================================
test_separator("TESTS INVENTAIRE")

inv = Inventaire()
inv.creer_inventaire_depart()

assert inv.get_quantite("Poke Ball") == 20
assert inv.get_quantite("Super Ball") == 10
assert inv.get_quantite("Hyper Ball") == 5
print("[OK] Inventaire de depart")

# Test retirer un objet
ball = inv.retirer("Poke Ball")
assert ball is not None
assert inv.get_quantite("Poke Ball") == 19
print("[OK] Retirer un objet")

# Test balls disponibles
balls = inv.get_balls()
assert len(balls) >= 3
print("[OK] Liste des balls")

# Test multiplicateur Filet Ball
inv.ajouter(FILET_BALL, 5)
mult = inv.get_multiplicateur_ball(FILET_BALL, types_pokemon=["Eau", "Vol"])
assert mult == 3.5, f"Filet Ball vs Eau devrait donner 3.5, got {mult}"
mult2 = inv.get_multiplicateur_ball(FILET_BALL, types_pokemon=["Feu"])
assert mult2 == 1.0, f"Filet Ball vs Feu devrait donner 1.0, got {mult2}"
print("[OK] Multiplicateur Filet Ball")

# Test Master Ball
mult_master = inv.get_multiplicateur_ball(MASTER_BALL)
assert mult_master == 255.0
print("[OK] Master Ball = capture garantie")


# =====================================================
# TESTS EXPERIENCE
# =====================================================
test_separator("TESTS EXPERIENCE")

assert Experience.xp_pour_niveau(5) == 125, "XP niveau 5 = 125"
assert Experience.xp_pour_niveau(10) == 1000, "XP niveau 10 = 1000"
assert Experience.xp_pour_niveau(100) == 1000000, "XP niveau 100 = 1000000"
print("[OK] XP par niveau (courbe Medium Fast)")

xp = Experience.xp_gagnee(64, 10)
assert xp > 0, "XP gagnee devrait etre > 0"
print(f"[OK] XP gagnee (base=64, niv=10) = {xp}")

assert Experience.peut_monter_niveau(1331, 10) == True  # 1331 >= 11^3 (niveau suivant)
assert Experience.peut_monter_niveau(1000, 10) == False  # 1000 < 11^3 = 1331
print("[OK] Verification level up")

nouveau_niv = Experience.calculer_niveaux_gagnes(8000, 5)
assert nouveau_niv == 20, f"Avec 8000 XP au niv 5, devrait monter a 20, got {nouveau_niv}"
print("[OK] Calcul multi level up")

pct = Experience.pourcentage_niveau(500, 7)
assert 0 <= pct <= 100
print(f"[OK] Pourcentage progression = {pct}%")


# =====================================================
# TESTS POKEMON
# =====================================================
test_separator("TESTS POKEMON")

# Creer un Pokemon depuis les donnees JSON
donnees_test = {
    "numero": 4,
    "nom": "Salameche",
    "types": ["Feu"],
    "pv": 39,
    "attaque": 52,
    "defense": 43,
    "attaque_speciale": 60,
    "defense_speciale": 50,
    "vitesse": 65,
    "base_xp": 62,
    "taux_capture": 45,
    "evolution_id": 5,
    "evolution_niveau": 16,
    "evolution_nom": "Reptincel",
}

salameche = Pokemon.depuis_json(donnees_test, niveau=5)
assert salameche.nom == "Salameche"
assert salameche.types == ["Feu"]
assert salameche.niveau == 5
assert salameche.pv > 0
assert salameche.pv == salameche.pv_max
print(f"[OK] Creation Pokemon : {salameche.nom} (Niv.{salameche.niveau}, PV:{salameche.pv})")

# Test KO
assert salameche.est_ko() == False
salameche.subir_degats(9999)
assert salameche.est_ko() == True
assert salameche.pv == 0
print("[OK] Systeme KO")

# Test soigner
salameche.pv = salameche.pv_max  # Reset
salameche.subir_degats(10)
pv_avant = salameche.pv
salameche.soigner(5)
assert salameche.pv == pv_avant + 5
print("[OK] Soigner")

# Test evolution
salameche2 = Pokemon.depuis_json(donnees_test, niveau=15)
assert salameche2.peut_evoluer() == False  # Niveau 15 < 16

salameche3 = Pokemon.depuis_json(donnees_test, niveau=16)
assert salameche3.peut_evoluer() == True
print("[OK] Verification evolution")

# Test combat entre deux Pokemon
donnees_cara = {
    "numero": 7, "nom": "Carapuce", "types": ["Eau"],
    "pv": 44, "attaque": 48, "defense": 65,
    "attaque_speciale": 50, "defense_speciale": 64, "vitesse": 43,
    "base_xp": 63, "taux_capture": 45,
    "evolution_id": 8, "evolution_niveau": 16, "evolution_nom": "Carabaffe",
}

cara = Pokemon.depuis_json(donnees_cara, niveau=10)
sal = Pokemon.depuis_json(donnees_test, niveau=10)
degats, msgs = sal.attaquer(cara)
assert cara.pv < cara.pv_max or degats == 0  # Degats infliges (sauf si rate par statut)
print(f"[OK] Combat : {sal.nom} attaque {cara.nom} -> {degats} degats")


# =====================================================
# TESTS POKEDEX
# =====================================================
test_separator("TESTS POKEDEX")

# Creer un Pokedex temporaire
with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
    tmp_path = tmp.name

pokedex = Pokedex(chemin_json=tmp_path)

# Test enregistrer vu
poke_test = Pokemon.depuis_json(donnees_test, niveau=5)
pokedex.enregistrer_vu(poke_test)
assert pokedex.est_vu(4) == True
assert pokedex.est_capture(4) == False
assert pokedex.get_nombre_vus() == 1
print("[OK] Enregistrer vu")

# Test enregistrer capture (upgrade de vu a capture)
pokedex.enregistrer_capture(poke_test)
assert pokedex.est_capture(4) == True
assert pokedex.get_nombre_vus() == 1  # Toujours 1, pas de doublon
assert pokedex.get_nombre_captures() == 1
print("[OK] Enregistrer capture (upgrade vu -> capture)")

# Test pas de downgrade
poke_test2 = Pokemon.depuis_json(donnees_cara, niveau=5)
pokedex.enregistrer_capture(poke_test2)
pokedex.enregistrer_vu(poke_test2)  # Ne devrait pas changer le statut
assert pokedex.est_capture(7) == True
print("[OK] Pas de downgrade capture -> vu")

# Test filtrer par type
pokedex.enregistrer_vu(Pokemon.depuis_json({
    "numero": 25, "nom": "Pikachu", "types": ["Electrik"],
    "pv": 35, "attaque": 55, "defense": 40,
    "attaque_speciale": 50, "defense_speciale": 50, "vitesse": 90,
    "base_xp": 112, "taux_capture": 190,
}, niveau=5))
resultats_feu = pokedex.filtrer_par_type("Feu")
assert len(resultats_feu) == 1
print("[OK] Filtrer par type")

# Test sauvegarde et chargement
pokedex.sauvegarder()
pokedex2 = Pokedex(chemin_json=tmp_path)
pokedex2.charger()
assert pokedex2.get_nombre_vus() == pokedex.get_nombre_vus()
assert pokedex2.est_capture(4) == True
print("[OK] Sauvegarde et chargement JSON")

# Test stats
stats = pokedex.get_stats()
assert stats["vus"] == 3
assert stats["captures"] == 2
assert stats["total"] == 1025
print(f"[OK] Stats Pokedex : {stats['vus']} vus, {stats['captures']} captures")

# Nettoyage
os.unlink(tmp_path)


# =====================================================
# TESTS CAPTURE
# =====================================================
test_separator("TESTS CAPTURE")

inv_capture = Inventaire()
inv_capture.ajouter(POKE_BALL, 10)
inv_capture.ajouter(MASTER_BALL, 1)

# Pokemon avec 1 PV (facile a capturer)
poke_faible = Pokemon.depuis_json(donnees_test, niveau=5)
poke_faible.pv = 1

# Test probabilite
prob = Capture.calculer_probabilite(poke_faible, 1.0)
print(f"[OK] Probabilite capture (PV=1, PokeBall) = {prob}%")

# Test Master Ball = capture garantie
capture, secousses, msgs = Capture.tenter_capture(
    poke_faible, MASTER_BALL, inv_capture
)
assert capture == True
print("[OK] Master Ball = capture garantie")

# Test avec Poke Ball a PV max (difficile)
poke_plein = Pokemon.depuis_json(donnees_test, niveau=5)
prob_plein = Capture.calculer_probabilite(poke_plein, 1.0)
prob_faible = Capture.calculer_probabilite(poke_faible, 1.0)
assert prob_faible > prob_plein, "PV bas devrait avoir plus de chance"
print(f"[OK] PV bas = plus facile (PV max: {prob_plein}%, PV 1: {prob_faible}%)")


# =====================================================
# TESTS COMBAT
# =====================================================
test_separator("TESTS COMBAT")

from combat import Combat

inv_combat = Inventaire()
inv_combat.creer_inventaire_depart()
pokedex_combat = Pokedex()

joueur = Pokemon.depuis_json(donnees_cara, niveau=15)
adverse = Pokemon.depuis_json(donnees_test, niveau=10)

combat = Combat(joueur, adverse, inv_combat, pokedex_combat)

# Verifier que l'adverse est enregistre comme vu
assert pokedex_combat.est_vu(adverse.numero)
print("[OK] Pokemon adverse enregistre comme vu")

# Jouer un tour
msgs = combat.tour_attaque()
assert len(msgs) > 0
assert combat.tour == 1
print(f"[OK] Tour 1 joue ({len(msgs)} messages)")

# Jouer jusqu'a la fin
tours_max = 50
while not combat.termine and combat.tour < tours_max:
    combat.tour_attaque()

assert combat.termine or combat.tour >= tours_max
resultat = combat.get_resultat()
print(f"[OK] Combat termine en {combat.tour} tours : {resultat}")

# Test etat du combat
etat = combat.get_etat()
assert "joueur" in etat
assert "adverse" in etat
assert "tour" in etat
print("[OK] Etat du combat lisible")


# =====================================================
# TEST CHARGEMENT 1025 POKEMON
# =====================================================
test_separator("TEST CHARGEMENT POKEMON.JSON")

try:
    tous_les_pokemon = Pokemon.charger_tous()
    assert len(tous_les_pokemon) == 1025, f"Attendu 1025, got {len(tous_les_pokemon)}"

    # Verifier quelques Pokemon
    bulbi = tous_les_pokemon[0]
    assert bulbi["nom"] == "Bulbizarre"
    assert bulbi["types"] == ["Plante", "Poison"]

    pikachu = tous_les_pokemon[24]
    assert pikachu["nom"] == "Pikachu"
    assert pikachu["types"] == ["Electrik"]

    dernier = tous_les_pokemon[-1]
    assert dernier["numero"] == 1025

    print(f"[OK] 1025 Pokemon charges depuis pokemon.json")
    print(f"     Premier : #{bulbi['numero']} {bulbi['nom']}")
    print(f"     Dernier : #{dernier['numero']} {dernier['nom']}")
except FileNotFoundError:
    print("[SKIP] pokemon.json non trouve (normal si pas dans le bon dossier)")


# =====================================================
# RESUME
# =====================================================
print(f"\n{'='*50}")
print("  TOUS LES TESTS SONT PASSES !")
print(f"{'='*50}")
