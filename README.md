# Pokemon - Projet Python

Jeu Pokemon en Python avec interface graphique Pygame. Combat tour par tour, capture, Pokedex et gestion d'inventaire.

## Equipe

| Dev | Role | Modules |
|-----|------|---------|
| Dev 1 | Interface graphique | `main.py`, `gui/` |
| Dev 2 | Navigation & UI logique | `navigation.py`, `barre_vie.py`, `sprites.py`, `ecran_pokedex.py` |
| Dev 3 | Logique metier | `type_chart.py`, `pokemon.py`, `combat.py`, `capture.py`, `pokedex.py`, `inventaire.py`, `experience.py`, `statut.py` |
| Dev 4 | Structure & tests | `config.py`, `utils.py`, `tests/`, `README.md` |

## Installation

```bash
git clone https://github.com/GA2207/Pokemon.git
cd Pokemon
```

Python 3.10+ requis. Dependance : Pygame.

```bash
pip install pygame
```

## Lancement

```bash
python main.py
```

## Fonctionnalites

- **Combat tour par tour** : systeme de types 18x18, STAB, coups critiques, statuts
- **Capture** : formule officielle avec Pokeballs, secousses, bonus statut
- **Pokedex** : 1025 Pokemon, distinction vu/capture, filtres par type, persistance JSON
- **Inventaire** : Pokeballs (7 types), potions, soins de statut, rappels
- **Experience** : courbe Medium Fast, montee de niveau, evolution
- **Interface Pygame** : menu, selection, combat, pokedex, victoire/defaite

## Structure du projet

```
Pokemon/
├── main.py                  # Point d'entree
├── config.py                # Configuration
├── utils.py                 # Utilitaires
├── type_chart.py            # Matrice 18x18 + couleurs types
├── statut.py                # Alterations de statut
├── inventaire.py            # Inventaire objets/balls
├── experience.py            # XP et niveaux
├── pokemon.py               # Classe Pokemon
├── pokedex.py               # Pokedex vu/capture
├── capture.py               # Systeme de capture
├── combat.py                # Systeme de combat
├── navigation.py            # Navigation ecrans
├── barre_vie.py             # Barres de vie
├── sprites.py               # Gestion sprites
├── ecran_pokedex.py         # Ecran Pokedex logique
├── gui/                     # Interface Pygame
│   ├── app.py               # Controleur principal
│   ├── composants.py        # Widgets reutilisables
│   ├── ecran_menu.py        # Menu principal
│   ├── ecran_selection.py   # Selection Pokemon
│   ├── ecran_combat.py      # Ecran combat
│   ├── ecran_pokedex_gui.py # Ecran Pokedex GUI
│   ├── ecran_victoire.py    # Ecran victoire
│   ├── ecran_defaite.py     # Ecran defaite
│   └── ecran_ajout.py       # Ajout Pokemon
├── data/
│   └── pokemon.json         # 1025 Pokemon
├── assets/sprites/           # Sprites Pokemon
├── tests.py                 # Tests Dev 3
└── tests/                   # Tests integration
```

## Tests

```bash
python tests.py                      # Tests unitaires Dev 3
python tests/test_dev2.py            # Tests Dev 2 adaptes
python tests/test_dev2_semaine2.py   # Tests semaine 2
python tests/test_integration.py     # Tests integration
```
