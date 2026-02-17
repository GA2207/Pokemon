"""
Module TypeChart - Tableau d'efficacite des 18 types Pokemon (Gen 6+).
Gere les multiplicateurs, faiblesses, resistances et immunites.
"""


class TypeChart:
    """Tableau d'efficacite des types Pokemon 18x18."""

    TYPES = [
        "Normal", "Feu", "Eau", "Plante", "Electrik", "Glace",
        "Combat", "Poison", "Sol", "Vol", "Psy", "Insecte",
        "Roche", "Spectre", "Dragon", "Tenebres", "Acier", "Fee"
    ]

    # Matrice 18x18 : CHART[attaquant][defenseur]
    # Ligne = type attaquant, Colonne = type defenseur
    CHART = [
        #          NOR  FEU  EAU  PLA  ELE  GLA  COM  POI  SOL  VOL  PSY  INS  ROC  SPE  DRA  TEN  ACI  FEE
        # Normal
        [1,    1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   0.5, 0,   1,   1,   0.5, 1],
        # Feu
        [1,    0.5, 0.5, 2,   1,   2,   1,   1,   1,   1,   1,   2,   0.5, 1,   0.5, 1,   2,   1],
        # Eau
        [1,    2,   0.5, 0.5, 1,   1,   1,   1,   2,   1,   1,   1,   2,   1,   0.5, 1,   1,   1],
        # Plante
        [1,    0.5, 2,   0.5, 1,   1,   1,   0.5, 2,   0.5, 1,   0.5, 2,   1,   0.5, 1,   0.5, 1],
        # Electrik
        [1,    1,   2,   0.5, 0.5, 1,   1,   1,   0,   2,   1,   1,   1,   1,   0.5, 1,   1,   1],
        # Glace
        [1,    0.5, 0.5, 2,   1,   0.5, 1,   1,   2,   2,   1,   1,   1,   1,   2,   1,   0.5, 1],
        # Combat
        [2,    1,   1,   1,   1,   2,   1,   0.5, 1,   0.5, 0.5, 0.5, 2,   0,   1,   2,   2,   0.5],
        # Poison
        [1,    1,   1,   2,   1,   1,   1,   0.5, 0.5, 1,   1,   1,   0.5, 0.5, 1,   1,   0,   2],
        # Sol
        [1,    2,   1,   0.5, 2,   1,   1,   2,   1,   0,   1,   0.5, 2,   1,   1,   1,   2,   1],
        # Vol
        [1,    1,   1,   2,   0.5, 1,   2,   1,   1,   1,   1,   2,   0.5, 1,   1,   1,   0.5, 1],
        # Psy
        [1,    1,   1,   1,   1,   1,   2,   2,   1,   1,   0.5, 1,   1,   1,   1,   0,   0.5, 1],
        # Insecte
        [1,    0.5, 1,   2,   1,   1,   0.5, 0.5, 1,   0.5, 2,   1,   1,   0.5, 1,   2,   0.5, 0.5],
        # Roche
        [1,    2,   1,   1,   1,   2,   0.5, 1,   0.5, 2,   1,   2,   1,   1,   1,   1,   0.5, 1],
        # Spectre
        [0,    1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   1,   1,   2,   1,   0.5, 1,   1],
        # Dragon
        [1,    1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   2,   1,   0.5, 0],
        # Tenebres
        [1,    1,   1,   1,   1,   1,   0.5, 1,   1,   1,   2,   1,   1,   2,   1,   0.5, 0.5, 0.5],
        # Acier
        [1,    0.5, 0.5, 1,   0.5, 2,   1,   1,   1,   1,   1,   1,   2,   1,   1,   1,   0.5, 2],
        # Fee
        [1,    0.5, 1,   1,   1,   1,   2,   0.5, 1,   1,   1,   1,   1,   1,   2,   2,   0.5, 1],
    ]

    @classmethod
    def get_index(cls, type_name):
        """Retourne l'index d'un type dans la matrice."""
        try:
            return cls.TYPES.index(type_name)
        except ValueError:
            return -1

    @classmethod
    def get_efficacite(cls, type_attaquant, type_defenseur):
        """Retourne le multiplicateur pour un type attaquant vs un type defenseur."""
        idx_att = cls.get_index(type_attaquant)
        idx_def = cls.get_index(type_defenseur)
        if idx_att < 0 or idx_def < 0:
            return 1.0
        return cls.CHART[idx_att][idx_def]

    @classmethod
    def get_multiplicateur(cls, type_attaquant, types_defenseur):
        """
        Retourne le multiplicateur total pour un type attaquant
        contre un defenseur ayant un ou deux types.
        En cas de double type, les multiplicateurs sont multiplies entre eux.
        Ex: Electrik vs Eau/Vol = 2 * 2 = 4
        """
        mult = 1.0
        for type_def in types_defenseur:
            mult *= cls.get_efficacite(type_attaquant, type_def)
        return mult

    @classmethod
    def get_faiblesses(cls, type_name):
        """Retourne la liste des types super efficaces (x2) contre ce type."""
        idx_def = cls.get_index(type_name)
        if idx_def < 0:
            return []
        faiblesses = []
        for i, type_att in enumerate(cls.TYPES):
            if cls.CHART[i][idx_def] == 2:
                faiblesses.append(type_att)
        return faiblesses

    @classmethod
    def get_resistances(cls, type_name):
        """Retourne la liste des types peu efficaces (x0.5) contre ce type."""
        idx_def = cls.get_index(type_name)
        if idx_def < 0:
            return []
        resistances = []
        for i, type_att in enumerate(cls.TYPES):
            if cls.CHART[i][idx_def] == 0.5:
                resistances.append(type_att)
        return resistances

    @classmethod
    def get_immunites(cls, type_name):
        """Retourne la liste des types sans effet (x0) contre ce type."""
        idx_def = cls.get_index(type_name)
        if idx_def < 0:
            return []
        immunites = []
        for i, type_att in enumerate(cls.TYPES):
            if cls.CHART[i][idx_def] == 0:
                immunites.append(type_att)
        return immunites

    @classmethod
    def get_message_efficacite(cls, multiplicateur):
        """Retourne le message d'efficacite selon le multiplicateur."""
        if multiplicateur == 0:
            return "Ca n'affecte pas le Pokemon..."
        elif multiplicateur == 0.25:
            return "Ce n'est vraiment pas efficace..."
        elif multiplicateur == 0.5:
            return "Ce n'est pas tres efficace..."
        elif multiplicateur == 1:
            return None
        elif multiplicateur == 2:
            return "C'est super efficace !"
        elif multiplicateur >= 4:
            return "C'est hyper efficace !!"
        return None

    @classmethod
    def est_type_valide(cls, type_name):
        """Verifie si un type existe dans le tableau."""
        return type_name in cls.TYPES
