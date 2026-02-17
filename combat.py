"""
Module Combat - Gere le deroulement d'un combat Pokemon complet.
Tour par tour avec vitesse, statuts, capture, objets et XP.
"""

import random

from type_chart import TypeChart
from capture import Capture
from experience import Experience


class Combat:
    """Gere un combat entre le Pokemon du joueur et un Pokemon sauvage/adverse."""

    def __init__(self, pokemon_joueur, pokemon_adverse, inventaire=None, pokedex=None):
        self.pokemon_joueur = pokemon_joueur
        self.pokemon_adverse = pokemon_adverse
        self.inventaire = inventaire
        self.pokedex = pokedex
        self.tour = 0
        self.termine = False
        self.vainqueur = None
        self.capture_reussie = False
        self.abandon = False
        self.log = []

        # Enregistrer le Pokemon adverse comme "vu" dans le Pokedex
        if self.pokedex:
            self.pokedex.enregistrer_vu(pokemon_adverse)

    def _ajouter_log(self, message):
        """Ajoute un message au journal de combat."""
        self.log.append(message)

    def _ajouter_logs(self, messages):
        """Ajoute plusieurs messages au journal."""
        for msg in messages:
            self.log.append(msg)

    def get_ordre_tour(self):
        """
        Determine quel Pokemon attaque en premier selon la vitesse.
        Retourne ("joueur", "adverse") ou ("adverse", "joueur").
        """
        vit_joueur = self.pokemon_joueur.get_vitesse_effective()
        vit_adverse = self.pokemon_adverse.get_vitesse_effective()

        if vit_joueur > vit_adverse:
            return "joueur", "adverse"
        elif vit_adverse > vit_joueur:
            return "adverse", "joueur"
        else:
            # Egalite : aleatoire
            if random.random() < 0.5:
                return "joueur", "adverse"
            return "adverse", "joueur"

    def jouer_tour_attaque(self, attaquant, defenseur, nom_attaquant):
        """
        Execute un tour d'attaque pour un Pokemon.
        Retourne les messages generes.
        """
        messages = []
        messages.append(f"\n--- Tour de {attaquant.nom} ---")

        # Attaque ratee (10% de chance)
        if random.random() < 0.10:
            messages.append(f"{attaquant.nom} rate son attaque !")
            return messages

        # Executer l'attaque
        degats, msgs_attaque = attaquant.attaquer(defenseur)
        messages.extend(msgs_attaque)

        return messages

    def appliquer_effets_fin_tour(self, pokemon, nom):
        """Applique les effets de statut en fin de tour."""
        messages = []
        degats, msg = pokemon.statut.appliquer_degats_fin_tour(pokemon.pv_max)
        if degats > 0:
            pokemon.subir_degats(degats)
            messages.append(msg)
            if pokemon.est_ko():
                messages.append(f"{pokemon.nom} est KO a cause de son statut !")
        return messages

    def tour_attaque(self):
        """
        Execute un tour de combat complet (les deux Pokemon attaquent).
        Retourne les messages du tour.
        """
        if self.termine:
            return ["Le combat est deja termine."]

        self.tour += 1
        messages = [f"\n{'='*40}\nTour {self.tour}\n{'='*40}"]

        premier, second = self.get_ordre_tour()

        if premier == "joueur":
            poke_1, poke_2 = self.pokemon_joueur, self.pokemon_adverse
            nom_1, nom_2 = "joueur", "adverse"
        else:
            poke_1, poke_2 = self.pokemon_adverse, self.pokemon_joueur
            nom_1, nom_2 = "adverse", "joueur"

        # Premier Pokemon attaque
        msgs = self.jouer_tour_attaque(poke_1, poke_2, nom_1)
        messages.extend(msgs)

        # Verifier KO
        if poke_2.est_ko():
            self._fin_combat(poke_1)
            self._ajouter_logs(messages)
            return messages

        # Effets fin de tour pour le premier
        msgs = self.appliquer_effets_fin_tour(poke_1, nom_1)
        messages.extend(msgs)
        if poke_1.est_ko():
            self._fin_combat(poke_2)
            self._ajouter_logs(messages)
            return messages

        # Second Pokemon attaque
        msgs = self.jouer_tour_attaque(poke_2, poke_1, nom_2)
        messages.extend(msgs)

        # Verifier KO
        if poke_1.est_ko():
            self._fin_combat(poke_2)
            self._ajouter_logs(messages)
            return messages

        # Effets fin de tour pour le second
        msgs = self.appliquer_effets_fin_tour(poke_2, nom_2)
        messages.extend(msgs)
        if poke_2.est_ko():
            self._fin_combat(poke_1)
            self._ajouter_logs(messages)
            return messages

        # Afficher les PV
        messages.append(f"\n{self.pokemon_joueur.nom}: {self.pokemon_joueur.pv}/{self.pokemon_joueur.pv_max} PV")
        messages.append(f"{self.pokemon_adverse.nom}: {self.pokemon_adverse.pv}/{self.pokemon_adverse.pv_max} PV")

        self._ajouter_logs(messages)
        return messages

    def tenter_capture(self, ball):
        """
        Le joueur tente de capturer le Pokemon adverse.
        Consomme la ball de l'inventaire.
        Retourne les messages.
        """
        if self.termine:
            return ["Le combat est deja termine."]

        messages = []
        self.tour += 1

        # Retirer la ball de l'inventaire
        ball_utilisee = self.inventaire.retirer(ball.nom) if self.inventaire else None
        if ball_utilisee is None:
            messages.append(f"Vous n'avez plus de {ball.nom} !")
            return messages

        # Tenter la capture
        capture, nb_secousses, msgs_capture = Capture.tenter_capture(
            self.pokemon_adverse,
            ball,
            self.inventaire,
            types_pokemon=self.pokemon_adverse.types,
            tour_combat=self.tour,
        )
        messages.extend(msgs_capture)

        if capture:
            self.capture_reussie = True
            self.termine = True

            # Enregistrer comme capture dans le Pokedex
            if self.pokedex:
                self.pokedex.enregistrer_capture(self.pokemon_adverse)
                messages.append(f"{self.pokemon_adverse.nom} est enregistre dans le Pokedex !")

            # Donner de l'XP
            xp = Experience.xp_gagnee(
                self.pokemon_adverse.base_xp,
                self.pokemon_adverse.niveau
            )
            msgs_xp = self.pokemon_joueur.gagner_xp(xp)
            messages.extend(msgs_xp)
        else:
            # Le Pokemon adverse attaque apres une capture ratee
            messages.append(f"\n{self.pokemon_adverse.nom} contre-attaque !")
            msgs = self.jouer_tour_attaque(
                self.pokemon_adverse, self.pokemon_joueur, "adverse"
            )
            messages.extend(msgs)

            if self.pokemon_joueur.est_ko():
                self._fin_combat(self.pokemon_adverse)

            # Effets fin de tour
            msgs = self.appliquer_effets_fin_tour(self.pokemon_adverse, "adverse")
            messages.extend(msgs)

        self._ajouter_logs(messages)
        return messages

    def utiliser_objet(self, objet, pokemon_cible=None):
        """
        Le joueur utilise un objet pendant le combat.
        Retourne les messages.
        """
        if self.termine:
            return ["Le combat est deja termine."]

        messages = []
        self.tour += 1

        if pokemon_cible is None:
            pokemon_cible = self.pokemon_joueur

        if objet.categorie == "soin_pv":
            succes, msg = self.inventaire.utiliser_potion(objet, pokemon_cible)
        elif objet.categorie == "soin_statut":
            succes, msg = self.inventaire.utiliser_soin_statut(objet, pokemon_cible)
        elif objet.categorie == "revive":
            succes, msg = self.inventaire.utiliser_rappel(objet, pokemon_cible)
        else:
            succes = False
            msg = "Cet objet ne peut pas etre utilise en combat."

        messages.append(msg)

        if succes:
            # Le Pokemon adverse attaque apres utilisation d'un objet
            messages.append(f"\n{self.pokemon_adverse.nom} attaque !")
            msgs = self.jouer_tour_attaque(
                self.pokemon_adverse, self.pokemon_joueur, "adverse"
            )
            messages.extend(msgs)

            if self.pokemon_joueur.est_ko():
                self._fin_combat(self.pokemon_adverse)

            # Effets fin de tour
            msgs = self.appliquer_effets_fin_tour(self.pokemon_joueur, "joueur")
            messages.extend(msgs)
            msgs = self.appliquer_effets_fin_tour(self.pokemon_adverse, "adverse")
            messages.extend(msgs)

        self._ajouter_logs(messages)
        return messages

    def abandonner(self):
        """Le joueur abandonne le combat."""
        self.termine = True
        self.abandon = True
        msg = "Vous avez fui le combat !"
        self._ajouter_log(msg)
        return [msg]

    def _fin_combat(self, vainqueur_pokemon):
        """Termine le combat et distribue l'XP."""
        self.termine = True
        self.vainqueur = vainqueur_pokemon

        # Si le joueur gagne, donner de l'XP
        if vainqueur_pokemon == self.pokemon_joueur and not self.capture_reussie:
            xp = Experience.xp_gagnee(
                self.pokemon_adverse.base_xp,
                self.pokemon_adverse.niveau
            )
            msgs_xp = self.pokemon_joueur.gagner_xp(xp)
            self._ajouter_logs(msgs_xp)

    def get_vainqueur(self):
        """Retourne le Pokemon vainqueur ou None."""
        return self.vainqueur

    def get_resultat(self):
        """Retourne un resume du combat."""
        if not self.termine:
            return "Le combat est en cours."

        if self.capture_reussie:
            return f"Vous avez capture {self.pokemon_adverse.nom} !"
        elif self.abandon:
            return "Vous avez fui le combat."
        elif self.vainqueur == self.pokemon_joueur:
            return f"{self.pokemon_joueur.nom} a gagne le combat !"
        else:
            return f"{self.pokemon_adverse.nom} a gagne. {self.pokemon_joueur.nom} est KO..."

    def get_etat(self):
        """Retourne l'etat actuel du combat pour l'interface."""
        return {
            "tour": self.tour,
            "termine": self.termine,
            "joueur": {
                "nom": self.pokemon_joueur.nom,
                "types": self.pokemon_joueur.types,
                "pv": self.pokemon_joueur.pv,
                "pv_max": self.pokemon_joueur.pv_max,
                "niveau": self.pokemon_joueur.niveau,
                "statut": self.pokemon_joueur.statut.get_nom_statut(),
            },
            "adverse": {
                "nom": self.pokemon_adverse.nom,
                "types": self.pokemon_adverse.types,
                "pv": self.pokemon_adverse.pv,
                "pv_max": self.pokemon_adverse.pv_max,
                "niveau": self.pokemon_adverse.niveau,
                "statut": self.pokemon_adverse.statut.get_nom_statut(),
            },
            "capture_reussie": self.capture_reussie,
            "vainqueur": self.vainqueur.nom if self.vainqueur else None,
        }
