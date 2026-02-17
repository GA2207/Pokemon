"""
Module Capture - Systeme de capture de Pokemon.
Formule officielle avec Pokeballs, statuts, et secousses.
"""

import random


class Capture:
    """Gere la logique de capture d'un Pokemon sauvage."""

    @staticmethod
    def tenter_capture(pokemon_cible, ball, inventaire,
                       types_pokemon=None, tour_combat=1, contexte=None):
        """
        Tente de capturer un Pokemon sauvage.

        Args:
            pokemon_cible: Le Pokemon sauvage a capturer
            ball: L'objet Pokeball utilise
            inventaire: L'inventaire du joueur (pour calculer le mult ball)
            types_pokemon: Les types du Pokemon cible (pour Filet Ball)
            tour_combat: Numero du tour actuel (pour Rapide Ball)
            contexte: "nuit_grotte" ou None (pour Sombre Ball)

        Returns:
            (capture: bool, nb_secousses: int, messages: list[str])
        """
        messages = []

        if types_pokemon is None:
            types_pokemon = pokemon_cible.types

        # Multiplicateur de la ball
        mult_ball = inventaire.get_multiplicateur_ball(
            ball, types_pokemon, tour_combat, contexte
        )

        # Master Ball = capture garantie
        if mult_ball >= 255:
            messages.append(f"Lancer de {ball.nom}...")
            messages.append("La Master Ball ne rate jamais !")
            messages.append(f"{pokemon_cible.nom} est capture !")
            return True, 3, messages

        # Taux de capture de l'espece (3 a 255)
        taux_espece = pokemon_cible.taux_capture

        # Bonus statut
        bonus_statut = pokemon_cible.statut.get_bonus_capture()

        # Ratio PV : plus les PV sont bas, plus c'est facile
        ratio_pv = (3 * pokemon_cible.pv_max - 2 * pokemon_cible.pv) / (3 * pokemon_cible.pv_max)

        # Calcul du taux a
        a = ratio_pv * taux_espece * mult_ball * bonus_statut

        messages.append(f"Lancer de {ball.nom}...")

        # Si a >= 255, capture garantie
        if a >= 255:
            messages.append(f"{pokemon_cible.nom} est capture !")
            return True, 3, messages

        # Calcul du seuil de secousse (b)
        # b = 65536 / (255 / a)^0.25
        if a <= 0:
            a = 1
        b = 65536 / ((255 / a) ** 0.1875)

        # 4 checks de secousse
        nb_secousses = 0
        for i in range(4):
            check = random.randint(0, 65535)
            if check < b:
                nb_secousses += 1
            else:
                break

        # Messages de secousses
        secousse_msgs = [
            "La Ball bouge...",
            "La Ball bouge encore...",
            "La Ball bouge une derniere fois...",
        ]

        for i in range(min(nb_secousses, 3)):
            messages.append(secousse_msgs[i])

        if nb_secousses >= 4:
            messages.append(f"Gotcha ! {pokemon_cible.nom} est capture !")
            return True, nb_secousses, messages
        else:
            messages.append(f"Mince ! {pokemon_cible.nom} s'est echappe !")
            return False, nb_secousses, messages

    @staticmethod
    def calculer_probabilite(pokemon_cible, mult_ball, bonus_statut=1.0):
        """
        Calcule la probabilite approximative de capture (pour affichage).
        Retourne un pourcentage (0-100).
        """
        taux_espece = pokemon_cible.taux_capture
        ratio_pv = (3 * pokemon_cible.pv_max - 2 * pokemon_cible.pv) / (3 * pokemon_cible.pv_max)

        a = ratio_pv * taux_espece * mult_ball * bonus_statut

        if a >= 255:
            return 100.0

        if a <= 0:
            return 0.0

        # Probabilite approximative = (a/255)^0.75 * 100
        prob = ((a / 255) ** 0.75) * 100
        return min(100.0, max(0.1, round(prob, 1)))
