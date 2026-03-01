"""
gui/ecran_ajout.py - Ecran pour ajouter un Pokemon au Pokedex (Pygame).
"""

import pygame

from navigation import Ecran
from pokemon import Pokemon
from gui.composants import Bouton, ChampTexte, ListeScrollable
from config import (WINDOW_WIDTH, WINDOW_HEIGHT, COULEUR_FOND, COULEUR_TEXTE,
                    COULEUR_TEXTE_GRIS, COULEUR_VERT, COULEUR_GRIS,
                    NIVEAU_DEPART)


class EcranAjout:
    """Ecran permettant de choisir un Pokemon et l'ajouter au Pokedex."""

    def __init__(self, navigation, tous_les_pokemon, pokedex):
        self.navigation = navigation
        self.tous_les_pokemon = tous_les_pokemon
        self.pokedex = pokedex
        self._selection_idx = -1
        self._liste_filtree = list(tous_les_pokemon)
        self._niveau = NIVEAU_DEPART

        # Composants
        self.champ_recherche = ChampTexte(180, 60, 260, 30, placeholder="Rechercher...")
        self.liste = ListeScrollable(20, 100, WINDOW_WIDTH - 40, 400)
        self._remplir_liste(self.tous_les_pokemon)

        self.btn_retour = Bouton(WINDOW_WIDTH // 2 - 230, 620, 160, 45,
                                 "Retour", COULEUR_GRIS)
        self.btn_ajouter = Bouton(WINDOW_WIDTH // 2 + 10, 620, 220, 45,
                                  "Ajouter au Pokedex", COULEUR_VERT, enabled=False)

        self.btn_niv_moins = Bouton(580, 60, 30, 30, "-", COULEUR_GRIS, taille_police=16)
        self.btn_niv_plus = Bouton(670, 60, 30, 30, "+", COULEUR_GRIS, taille_police=16)

        self._info_texte = "Selectionnez un Pokemon"
        self._msg_texte = ""
        self._msg_couleur = COULEUR_VERT
        self._ancien_texte = ""

    def _remplir_liste(self, pokemon_list):
        items = []
        for p in pokemon_list:
            numero = str(p["numero"]).zfill(3)
            types_str = "/".join(p["types"])
            items.append(f"#{numero}  {p['nom']:<16} {types_str}")
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

        # Niveau
        if self.btn_niv_moins.handle_event(event):
            self._niveau = max(1, self._niveau - 1)
        if self.btn_niv_plus.handle_event(event):
            self._niveau = min(100, self._niveau + 1)

        # Liste
        if self.liste.handle_event(event):
            idx = self.liste.get_selection()
            if 0 <= idx < len(self._liste_filtree):
                self._selection_idx = idx
                d = self._liste_filtree[idx]
                types_str = "/".join(d["types"])
                self._info_texte = f"#{str(d['numero']).zfill(3)} {d['nom']} ({types_str})"
                self.btn_ajouter.enabled = True
                self._msg_texte = ""

        # Boutons
        if self.btn_retour.handle_event(event):
            self.navigation.retour()
        if self.btn_ajouter.handle_event(event):
            self._ajouter()

    def _ajouter(self):
        if self._selection_idx < 0 or self._selection_idx >= len(self._liste_filtree):
            return

        donnees = self._liste_filtree[self._selection_idx]
        pokemon = Pokemon.depuis_json(donnees, niveau=self._niveau)
        self.pokedex.enregistrer_capture(pokemon)
        self.pokedex.sauvegarder()

        self._msg_texte = f"{pokemon.nom} (Niv.{self._niveau}) ajoute au Pokedex !"
        self._msg_couleur = COULEUR_VERT

    def update(self):
        pass

    def draw(self, surface):
        surface.fill(COULEUR_FOND)

        # Titre
        font_titre = pygame.font.SysFont("Arial", 24, bold=True)
        titre = font_titre.render("Ajouter un Pokemon au Pokedex", True, COULEUR_TEXTE)
        surface.blit(titre, (20, 15))

        # Recherche
        font_label = pygame.font.SysFont("Arial", 14)
        lbl = font_label.render("Rechercher :", True, COULEUR_TEXTE)
        surface.blit(lbl, (20, 66))
        self.champ_recherche.draw(surface)

        # Niveau
        lbl_niv = font_label.render("Niveau :", True, COULEUR_TEXTE)
        surface.blit(lbl_niv, (500, 66))
        self.btn_niv_moins.draw(surface)
        font_niv = pygame.font.SysFont("Arial", 16, bold=True)
        niv_txt = font_niv.render(str(self._niveau), True, COULEUR_TEXTE)
        surface.blit(niv_txt, (625, 64))
        self.btn_niv_plus.draw(surface)

        # Liste
        self.liste.draw(surface)

        # Info
        font_info = pygame.font.SysFont("Arial", 14)
        couleur = COULEUR_TEXTE if self._selection_idx >= 0 else COULEUR_TEXTE_GRIS
        info_surf = font_info.render(self._info_texte, True, couleur)
        surface.blit(info_surf, (20, 515))

        # Message
        if self._msg_texte:
            msg_surf = font_info.render(self._msg_texte, True, self._msg_couleur)
            surface.blit(msg_surf, (20, 545))

        # Boutons
        self.btn_retour.draw(surface)
        self.btn_ajouter.draw(surface)
