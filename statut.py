"""
Module Statut - Systeme d'alterations de statut Pokemon.
Gere les 5 statuts principaux (persistants) et les statuts volatils.
"""

import random


class Statut:
    """Represente une alteration de statut sur un Pokemon."""

    # Statuts principaux (un seul a la fois, persiste apres combat)
    POISON = "poison"
    BRULURE = "brulure"
    PARALYSIE = "paralysie"
    SOMMEIL = "sommeil"
    GEL = "gel"

    # Statuts volatils (peuvent se cumuler, disparaissent au switch/fin combat)
    CONFUSION = "confusion"

    STATUTS_PRINCIPAUX = [POISON, BRULURE, PARALYSIE, SOMMEIL, GEL]
    STATUTS_VOLATILS = [CONFUSION]

    # Immunites par type
    IMMUNITES_TYPE = {
        POISON: ["Poison", "Acier"],
        BRULURE: ["Feu"],
        PARALYSIE: ["Electrik"],
        GEL: ["Glace"],
    }

    # Bonus capture par statut
    BONUS_CAPTURE = {
        SOMMEIL: 2.0,
        GEL: 2.0,
        POISON: 1.5,
        BRULURE: 1.5,
        PARALYSIE: 1.5,
    }

    def __init__(self):
        self.statut_principal = None
        self.tours_restants = 0  # Pour sommeil et confusion
        self.confusion = False
        self.tours_confusion = 0

    def appliquer_statut_principal(self, statut, types_pokemon):
        """
        Tente d'appliquer un statut principal.
        Retourne True si le statut a ete applique, False sinon.
        """
        # Verifier si deja un statut principal
        if self.statut_principal is not None:
            return False

        # Verifier immunite par type
        types_immuns = self.IMMUNITES_TYPE.get(statut, [])
        for t in types_pokemon:
            if t in types_immuns:
                return False

        self.statut_principal = statut

        # Definir la duree pour les statuts temporaires
        if statut == self.SOMMEIL:
            self.tours_restants = random.randint(1, 3)
        elif statut == self.GEL:
            self.tours_restants = 0  # Gere par chance de degel

        return True

    def appliquer_confusion(self):
        """Applique la confusion (statut volatil, cumulable avec un statut principal)."""
        if self.confusion:
            return False
        self.confusion = True
        self.tours_confusion = random.randint(1, 4)
        return True

    def retirer_statut_principal(self):
        """Retire le statut principal."""
        self.statut_principal = None
        self.tours_restants = 0

    def retirer_confusion(self):
        """Retire la confusion."""
        self.confusion = False
        self.tours_confusion = 0

    def retirer_tout(self):
        """Retire tous les statuts."""
        self.retirer_statut_principal()
        self.retirer_confusion()

    def peut_agir(self):
        """
        Verifie si le Pokemon peut agir ce tour.
        Retourne (peut_agir: bool, message: str ou None).
        """
        # Sommeil
        if self.statut_principal == self.SOMMEIL:
            if self.tours_restants > 0:
                self.tours_restants -= 1
                if self.tours_restants == 0:
                    self.retirer_statut_principal()
                    return True, "Le Pokemon se reveille !"
                return False, "Le Pokemon dort profondement..."

        # Gel
        if self.statut_principal == self.GEL:
            if random.random() < 0.20:
                self.retirer_statut_principal()
                return True, "Le Pokemon est degivre !"
            return False, "Le Pokemon est gele et ne peut pas bouger !"

        # Paralysie (25% de ne pas agir)
        if self.statut_principal == self.PARALYSIE:
            if random.random() < 0.25:
                return False, "Le Pokemon est paralyse ! Il ne peut pas attaquer !"

        # Confusion
        if self.confusion:
            self.tours_confusion -= 1
            if self.tours_confusion <= 0:
                self.retirer_confusion()
                return True, "Le Pokemon n'est plus confus !"

            if random.random() < 0.33:
                return False, "CONFUSION"  # Signal special : le Pokemon se frappe

        return True, None

    def appliquer_degats_fin_tour(self, pv_max):
        """
        Applique les degats de statut en fin de tour.
        Retourne (degats: int, message: str ou None).
        """
        if self.statut_principal == self.POISON:
            degats = max(1, pv_max // 8)
            return degats, f"Le Pokemon souffre du poison ! (-{degats} PV)"

        if self.statut_principal == self.BRULURE:
            degats = max(1, pv_max // 16)
            return degats, f"Le Pokemon souffre de sa brulure ! (-{degats} PV)"

        return 0, None

    def get_modificateur_attaque(self):
        """Retourne le modificateur d'attaque physique (brulure = /2)."""
        if self.statut_principal == self.BRULURE:
            return 0.5
        return 1.0

    def get_modificateur_vitesse(self):
        """Retourne le modificateur de vitesse (paralysie = /2)."""
        if self.statut_principal == self.PARALYSIE:
            return 0.5
        return 1.0

    def get_bonus_capture(self):
        """Retourne le bonus de capture lie au statut."""
        if self.statut_principal:
            return self.BONUS_CAPTURE.get(self.statut_principal, 1.0)
        return 1.0

    def get_nom_statut(self):
        """Retourne le nom du statut principal actuel."""
        noms = {
            self.POISON: "Empoisonne",
            self.BRULURE: "Brule",
            self.PARALYSIE: "Paralyse",
            self.SOMMEIL: "Endormi",
            self.GEL: "Gele",
        }
        if self.statut_principal:
            return noms.get(self.statut_principal, self.statut_principal)
        return None

    def __str__(self):
        parts = []
        if self.statut_principal:
            parts.append(self.get_nom_statut())
        if self.confusion:
            parts.append("Confus")
        return " | ".join(parts) if parts else "Aucun"
