"""
gui/ecran_selection.py - Ecran de selection du Pokemon pour le combat (Pygame).
"""

import pygame
import random

from navigation import Ecran
from pokemon import Pokemon
from gui.composants import Bouton, ChampTexte, ListeScrollable
from config import (WINDOW_WIDTH, WINDOW_HEIGHT, COULEUR_FOND, COULEUR_TEXTE,
                    COULEUR_TEXTE_GRIS, COULEUR_ROUGE, COULEUR_GRIS,
                    NIVEAU_DEPART)


class EcranSelection:
    """Selection du Pokemon du joueur + adversaire aleatoire."""

    def __init__(self, navigation, tous_les_pokemon, inventaire, pokedex):
        self.navigation = navigation
        self.tous_les_pokemon = tous_les_pokemon
        self.inventaire = inventaire
        self.pokedex = pokedex
        self._selection_idx = -1
        self._liste_filtree = list(tous_les_pokemon)

        # Composants
        self.champ_recherche = ChampTexte(200, 60, 300, 30, placeholder="Rechercher...")
        self.liste = ListeScrollable(40, 100, WINDOW_WIDTH - 80, 440)
        self._remplir_liste(self.tous_les_pokemon)

        self.btn_retour = Bouton(WINDOW_WIDTH // 2 - 200, 620, 160, 45,
                                 "Retour", COULEUR_GRIS)
        self.btn_combattre = Bouton(WINDOW_WIDTH // 2 + 40, 620, 160, 45,
                                    "Combattre !", COULEUR_ROUGE, enabled=False)

        self._info_texte = "Selectionnez un Pokemon dans la liste"
        self._ancien_texte = ""

    def _remplir_liste(self, pokemon_list):
        items = []
        for p in pokemon_list:
            numero = str(p["numero"]).zfill(3)
            types_str = "/".join(p["types"])
            items.append(f"#{numero}  {p['nom']:<16} {types_str:<20} PV:{p['pv']:>3}")
        self.liste.set_items(items)

    def handle_event(self, event):
        # Recherche
        if self.champ_recherche.handle_event(event):
            terme = self.champ_recherche.texte.lower()
            if terme != self._ancien_texte:
                self._ancien_texte = terme
                if not terme:
                    self._liste_filtree = list(self.tous_les_pokemon)
                else:
                    self._liste_filtree = [
                        p for p in self.tous_les_pokemon
                        if terme in p["nom"].lower() or terme in str(p["numero"])
                    ]
                self._remplir_liste(self._liste_filtree)

        # Liste
        if self.liste.handle_event(event):
            idx = self.liste.get_selection()
            if 0 <= idx < len(self._liste_filtree):
                self._selection_idx = idx
                d = self._liste_filtree[idx]
                types_str = "/".join(d["types"])
                self._info_texte = (
                    f"#{str(d['numero']).zfill(3)} {d['nom']} ({types_str}) "
                    f"- PV:{d['pv']} ATK:{d['attaque']} DEF:{d['defense']}"
                )
                self.btn_combattre.enabled = True

        # Boutons
        if self.btn_retour.handle_event(event):
            self.navigation.retour()
        if self.btn_combattre.handle_event(event):
            self._lancer_combat()

    def _lancer_combat(self):
        if self._selection_idx < 0 or self._selection_idx >= len(self._liste_filtree):
            return

        donnees_joueur = self._liste_filtree[self._selection_idx]
        pokemon_joueur = Pokemon.depuis_json(donnees_joueur, niveau=NIVEAU_DEPART)

        donnees_adverse = random.choice(self.tous_les_pokemon)
        niveau_adverse = random.randint(max(1, NIVEAU_DEPART - 2), NIVEAU_DEPART + 3)
        pokemon_adverse = Pokemon.depuis_json(donnees_adverse, niveau=niveau_adverse)

        self.navigation.aller_a(Ecran.COMBAT, {
            "pokemon_joueur": pokemon_joueur,
            "pokemon_adverse": pokemon_adverse,
        })

    def update(self):
        pass

    def draw(self, surface):
        surface.fill(COULEUR_FOND)

        # Titre
        font_titre = pygame.font.SysFont("Arial", 24, bold=True)
        titre = font_titre.render("Choisissez votre Pokemon", True, COULEUR_TEXTE)
        surface.blit(titre, (40, 20))

        # Recherche
        font_label = pygame.font.SysFont("Arial", 14)
        lbl = font_label.render("Rechercher :", True, COULEUR_TEXTE)
        surface.blit(lbl, (40, 66))
        self.champ_recherche.draw(surface)

        # Liste
        self.liste.draw(surface)

        # Info selection
        font_info = pygame.font.SysFont("Arial", 14)
        couleur = COULEUR_TEXTE if self._selection_idx >= 0 else COULEUR_TEXTE_GRIS
        info_surf = font_info.render(self._info_texte, True, couleur)
        surface.blit(info_surf, (40, 555))

        # Boutons
        self.btn_retour.draw(surface)
        self.btn_combattre.draw(surface)
