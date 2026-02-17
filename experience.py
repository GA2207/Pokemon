"""
Module Experience - Systeme d'XP et de montee de niveau.
Courbe Medium Fast (XP pour niveau N = N^3).
"""


class Experience:
    """Gere le systeme d'experience et de montee de niveau."""

    NIVEAU_MAX = 100

    @staticmethod
    def xp_pour_niveau(niveau):
        """Retourne l'XP totale necessaire pour atteindre un niveau (courbe Medium Fast)."""
        return niveau ** 3

    @staticmethod
    def xp_gagnee(base_xp_vaincu, niveau_vaincu, nb_participants=1, est_combat_dresseur=False):
        """
        Calcule l'XP gagnee apres avoir vaincu un Pokemon.

        Args:
            base_xp_vaincu: XP de base du Pokemon vaincu (specifique a l'espece)
            niveau_vaincu: Niveau du Pokemon vaincu
            nb_participants: Nombre de Pokemon ayant participe au combat
            est_combat_dresseur: True si combat contre un dresseur (bonus x1.5)

        Returns:
            int: Points d'experience gagnes
        """
        xp = (base_xp_vaincu * niveau_vaincu) / (7 * max(1, nb_participants))

        if est_combat_dresseur:
            xp *= 1.5

        return max(1, int(xp))

    @staticmethod
    def peut_monter_niveau(xp_actuelle, niveau_actuel):
        """Verifie si le Pokemon peut monter de niveau."""
        if niveau_actuel >= Experience.NIVEAU_MAX:
            return False
        xp_requise = Experience.xp_pour_niveau(niveau_actuel + 1)
        return xp_actuelle >= xp_requise

    @staticmethod
    def calculer_niveaux_gagnes(xp_actuelle, niveau_actuel):
        """
        Calcule combien de niveaux le Pokemon gagne d'un coup.
        Retourne le nouveau niveau.
        """
        nouveau_niveau = niveau_actuel
        while nouveau_niveau < Experience.NIVEAU_MAX:
            xp_requise = Experience.xp_pour_niveau(nouveau_niveau + 1)
            if xp_actuelle >= xp_requise:
                nouveau_niveau += 1
            else:
                break
        return nouveau_niveau

    @staticmethod
    def calculer_nouvelles_stats(stats_base, ancien_niveau, nouveau_niveau):
        """
        Recalcule les stats apres une montee de niveau.
        Formule simplifiee : stat = (stat_base * 2 * niveau / 100) + 5
        Pour les PV : stat = (stat_base * 2 * niveau / 100) + niveau + 10

        Args:
            stats_base: dict avec les stats de base du Pokemon
            ancien_niveau: Niveau avant le level up
            nouveau_niveau: Nouveau niveau

        Returns:
            dict: Nouvelles stats calculees
        """
        nouvelles_stats = {}

        for stat_nom, stat_base in stats_base.items():
            if stat_nom == "pv":
                # Formule PV
                new_val = int((stat_base * 2 * nouveau_niveau / 100) + nouveau_niveau + 10)
            else:
                # Formule autres stats
                new_val = int((stat_base * 2 * nouveau_niveau / 100) + 5)

            nouvelles_stats[stat_nom] = max(1, new_val)

        return nouvelles_stats

    @staticmethod
    def xp_restante_pour_prochain_niveau(xp_actuelle, niveau_actuel):
        """Retourne l'XP manquante pour le prochain niveau."""
        if niveau_actuel >= Experience.NIVEAU_MAX:
            return 0
        xp_requise = Experience.xp_pour_niveau(niveau_actuel + 1)
        return max(0, xp_requise - xp_actuelle)

    @staticmethod
    def pourcentage_niveau(xp_actuelle, niveau_actuel):
        """Retourne le pourcentage de progression vers le prochain niveau (0-100)."""
        if niveau_actuel >= Experience.NIVEAU_MAX:
            return 100
        xp_debut = Experience.xp_pour_niveau(niveau_actuel)
        xp_fin = Experience.xp_pour_niveau(niveau_actuel + 1)
        diff_total = xp_fin - xp_debut
        if diff_total <= 0:
            return 100
        diff_actuel = xp_actuelle - xp_debut
        return min(100, max(0, int((diff_actuel / diff_total) * 100)))
