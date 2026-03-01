"""
gui/ecran_combat.py - Ecran de combat Pokemon (Pygame).
"""

import pygame

from navigation import Ecran
from combat import Combat
from sprites import SpriteManager
from gui.composants import Bouton, BarreVieWidget, ZoneLog, dessiner_badge_type
from config import (WINDOW_WIDTH, WINDOW_HEIGHT, COULEUR_FOND, COULEUR_TEXTE,
                    COULEUR_ROUGE, COULEUR_BLEU, COULEUR_VERT, COULEUR_GRIS,
                    COULEUR_FOND_CLAIR)


class EcranCombatGUI:
    """Ecran de combat complet avec barres PV, sprites ASCII, actions et log."""

    def __init__(self, navigation, donnees, inventaire, pokedex):
        self.navigation = navigation
        self.inventaire = inventaire
        self.pokedex = pokedex

        self.pokemon_joueur = donnees["pokemon_joueur"]
        self.pokemon_adverse = donnees["pokemon_adverse"]

        self.combat = Combat(
            self.pokemon_joueur, self.pokemon_adverse,
            self.inventaire, self.pokedex
        )

        self.sprite_manager = SpriteManager(mode_gui="terminal")

        # Barres de vie
        self.barre_adverse = BarreVieWidget(480, 45, 280, 20)
        self.barre_joueur = BarreVieWidget(40, 415, 280, 20)

        # Boutons d'action
        bx = WINDOW_WIDTH - 340
        self.btn_attaquer = Bouton(bx, 380, 150, 42, "Attaquer", COULEUR_ROUGE)
        self.btn_capturer = Bouton(bx + 160, 380, 150, 42, "Capturer", COULEUR_BLEU)
        self.btn_objets = Bouton(bx, 430, 150, 42, "Objets", COULEUR_VERT)
        self.btn_fuir = Bouton(bx + 160, 430, 150, 42, "Abandonner", COULEUR_GRIS)

        # Log
        self.log = ZoneLog(20, 490, WINDOW_WIDTH - 40, 190)
        self.log.ajouter("Le combat commence !")
        self.log.ajouter(
            f"{self.pokemon_joueur.nom} (Niv.{self.pokemon_joueur.niveau}) "
            f"VS {self.pokemon_adverse.nom} (Niv.{self.pokemon_adverse.niveau})"
        )

        self._combat_fini = False
        self._timer_fin = 0

    def handle_event(self, event):
        self.log.handle_event(event)

        if self._combat_fini:
            return

        if self.btn_attaquer.handle_event(event):
            self._attaquer()
        elif self.btn_capturer.handle_event(event):
            self._capturer()
        elif self.btn_objets.handle_event(event):
            self._utiliser_objet()
        elif self.btn_fuir.handle_event(event):
            self._abandonner()

    def _attaquer(self):
        messages = self.combat.tour_attaque()
        self.log.ajouter_plusieurs(messages)
        self._verifier_fin()

    def _capturer(self):
        balls = self.inventaire.get_balls()
        if not balls:
            self.log.ajouter("Vous n'avez plus de Pokeball !")
            return
        ball, qty = balls[0]
        messages = self.combat.tenter_capture(ball)
        self.log.ajouter_plusieurs(messages)
        self._verifier_fin()

    def _utiliser_objet(self):
        objets = self.inventaire.get_objets_soin()
        if not objets:
            self.log.ajouter("Vous n'avez pas d'objets de soin !")
            return
        objet, qty = objets[0]
        messages = self.combat.utiliser_objet(objet)
        self.log.ajouter_plusieurs(messages)
        self._verifier_fin()

    def _abandonner(self):
        messages = self.combat.abandonner()
        self.log.ajouter_plusieurs(messages)
        self._combat_fini = True
        self._timer_fin = pygame.time.get_ticks()

    def _verifier_fin(self):
        if self.combat.termine:
            self._combat_fini = True
            self.log.ajouter(self.combat.get_resultat())
            self._timer_fin = pygame.time.get_ticks()

    def _desactiver_boutons(self):
        self.btn_attaquer.enabled = False
        self.btn_capturer.enabled = False
        self.btn_objets.enabled = False
        self.btn_fuir.enabled = False

    def update(self):
        if self._combat_fini:
            self._desactiver_boutons()
            if pygame.time.get_ticks() - self._timer_fin > 2000:
                self._naviguer_fin()

    def _naviguer_fin(self):
        donnees = {
            "pokemon_joueur": self.pokemon_joueur,
            "pokemon_adverse": self.pokemon_adverse,
            "combat": self.combat,
        }
        if self.combat.abandon:
            self.navigation.reset()
        elif self.combat.vainqueur == self.pokemon_joueur or self.combat.capture_reussie:
            self.navigation.remplacer(Ecran.VICTOIRE, donnees)
        else:
            self.navigation.remplacer(Ecran.DEFAITE, donnees)

    def draw(self, surface):
        surface.fill(COULEUR_FOND)
        font_nom = pygame.font.SysFont("Arial", 16, bold=True)
        font_info = pygame.font.SysFont("Arial", 12)
        font_sprite = pygame.font.SysFont("Courier New", 14)

        # === Zone adversaire (haut droit) ===
        nom_adv = font_nom.render(
            f"{self.pokemon_adverse.nom}  Niv.{self.pokemon_adverse.niveau}",
            True, COULEUR_TEXTE)
        surface.blit(nom_adv, (480, 15))

        # Types adverse
        tx = 480
        for t in self.pokemon_adverse.types:
            tx += dessiner_badge_type(surface, t, tx, 75)

        self.barre_adverse.draw(surface,
                                self.pokemon_adverse.pv, self.pokemon_adverse.pv_max)

        statut_a = self.pokemon_adverse.statut.get_nom_statut()
        if statut_a:
            s = font_info.render(statut_a, True, (255, 170, 0))
            surface.blit(s, (480, 95))

        # === Zone joueur (bas gauche) ===
        nom_j = font_nom.render(
            f"{self.pokemon_joueur.nom}  Niv.{self.pokemon_joueur.niveau}",
            True, COULEUR_TEXTE)
        surface.blit(nom_j, (40, 385))

        tx = 40
        for t in self.pokemon_joueur.types:
            tx += dessiner_badge_type(surface, t, tx, 445)

        self.barre_joueur.draw(surface,
                               self.pokemon_joueur.pv, self.pokemon_joueur.pv_max)

        statut_j = self.pokemon_joueur.statut.get_nom_statut()
        if statut_j:
            s = font_info.render(statut_j, True, (255, 170, 0))
            surface.blit(s, (40, 465))

        # === Zone sprites ASCII (centre) ===
        pygame.draw.rect(surface, COULEUR_FOND_CLAIR,
                         (20, 120, WINDOW_WIDTH - 40, 250), border_radius=8)

        sprite_j = self.sprite_manager.get_sprite_ascii(
            str(self.pokemon_joueur.numero).zfill(3))
        sprite_a = self.sprite_manager.get_sprite_ascii(
            str(self.pokemon_adverse.numero).zfill(3))

        # Joueur a gauche
        for i, ligne in enumerate(sprite_j):
            txt = font_sprite.render(ligne, True, (200, 220, 255))
            surface.blit(txt, (100, 150 + i * 22))
        nom_txt = font_info.render(self.pokemon_joueur.nom, True, COULEUR_TEXTE)
        surface.blit(nom_txt, (100, 150 + len(sprite_j) * 22 + 5))

        # Adverse a droite
        for i, ligne in enumerate(sprite_a):
            txt = font_sprite.render(ligne, True, (255, 200, 200))
            surface.blit(txt, (WINDOW_WIDTH - 250, 150 + i * 22))
        nom_txt = font_info.render(self.pokemon_adverse.nom, True, COULEUR_TEXTE)
        surface.blit(nom_txt, (WINDOW_WIDTH - 250, 150 + len(sprite_a) * 22 + 5))

        # === Boutons ===
        self.btn_attaquer.draw(surface)
        self.btn_capturer.draw(surface)
        self.btn_objets.draw(surface)
        self.btn_fuir.draw(surface)

        # === Log ===
        lbl = font_info.render("Journal de combat", True, (170, 170, 170))
        surface.blit(lbl, (20, 475))
        self.log.draw(surface)
