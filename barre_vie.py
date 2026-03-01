"""
barre_vie.py - Composant visuel barre de vie avec gradient (vert → jaune → rouge)
Dev 2 - Projet Pokemon - Semaine 2, Mardi

Gère l'affichage des PV en terminal et fournit les données pour l'interface GUI.
Seuils officiels : >50% vert, 20-50% jaune, <20% rouge (cf. documentation).
"""

# ─── Constantes de couleurs ────────────────────────────────────────────────────

COULEUR_PV_HAUTE  = "#16A34A"   # Vert  (>50%)
COULEUR_PV_MOYENNE = "#EAB308"  # Jaune (20-50%)
COULEUR_PV_BASSE   = "#DC2626"  # Rouge (<20%)

SEUIL_VERT   = 0.50   # 50% → vert
SEUIL_JAUNE  = 0.20   # 20% → rouge


# ─── Classe BarreVie ──────────────────────────────────────────────────────────

class BarreVie:
    """
    Composant de barre de vie pour un Pokémon.

    Gère le calcul du pourcentage de PV, la couleur associée,
    et l'affichage textuel en terminal (ASCII art).
    Fournit également les données nécessaires pour l'interface GUI.

    Seuils de couleur (selon la documentation) :
        > 50%     → Vert  (#16A34A)
        20% - 50% → Jaune (#EAB308)
        < 20%     → Rouge (#DC2626)
    """

    LARGEUR_BARRE = 20  # Nombre de blocs dans la barre ASCII

    def __init__(self, pv_max: int, pv_actuel: int = None, nom: str = ""):
        """
        Initialise la barre de vie.

        Args:
            pv_max (int): Points de vie maximum du Pokémon.
            pv_actuel (int): PV actuels (par défaut = pv_max).
            nom (str): Nom du Pokémon (pour l'affichage).
        """
        if pv_max <= 0:
            raise ValueError(f"[BarreVie] pv_max doit être > 0, reçu : {pv_max}")

        self._pv_max = pv_max
        self._pv_actuel = pv_actuel if pv_actuel is not None else pv_max
        self._nom = nom

        # Clampe entre 0 et pv_max
        self._pv_actuel = max(0, min(self._pv_max, self._pv_actuel))

    # ── Propriétés ─────────────────────────────────────────────────────────────

    @property
    def pv_actuel(self) -> int:
        """PV actuels du Pokémon."""
        return self._pv_actuel

    @pv_actuel.setter
    def pv_actuel(self, valeur: int):
        """Met à jour les PV actuels en clampant entre 0 et pv_max."""
        self._pv_actuel = max(0, min(self._pv_max, int(valeur)))

    @property
    def pv_max(self) -> int:
        """PV maximum du Pokémon."""
        return self._pv_max

    @property
    def nom(self) -> str:
        """Nom du Pokémon."""
        return self._nom

    # ── Calculs ────────────────────────────────────────────────────────────────

    def get_pourcentage(self) -> float:
        """
        Retourne le pourcentage de PV restants (0.0 à 1.0).

        Returns:
            float: Ex. 0.75 pour 75% de PV.
        """
        return self._pv_actuel / self._pv_max

    def get_pourcentage_affichage(self) -> int:
        """
        Retourne le pourcentage arrondi pour l'affichage (0 à 100).

        Returns:
            int: Ex. 75 pour 75%.
        """
        return round(self.get_pourcentage() * 100)

    def get_couleur_hex(self) -> str:
        """
        Retourne la couleur hexadécimale selon le pourcentage de PV.

        Returns:
            str: Code hex de la couleur (#16A34A, #EAB308, ou #DC2626).
        """
        pct = self.get_pourcentage()
        if pct > SEUIL_VERT:
            return COULEUR_PV_HAUTE
        elif pct > SEUIL_JAUNE:
            return COULEUR_PV_MOYENNE
        else:
            return COULEUR_PV_BASSE

    def get_etat(self) -> str:
        """
        Retourne l'état textuel des PV.

        Returns:
            str: 'haute', 'moyenne', ou 'basse'.
        """
        pct = self.get_pourcentage()
        if pct > SEUIL_VERT:
            return "haute"
        elif pct > SEUIL_JAUNE:
            return "moyenne"
        else:
            return "basse"

    def est_ko(self) -> bool:
        """
        Indique si le Pokémon est KO (PV = 0).

        Returns:
            bool: True si PV = 0.
        """
        return self._pv_actuel == 0

    # ── Affichage terminal ─────────────────────────────────────────────────────

    def afficher(self):
        """
        Affiche la barre de vie en ASCII dans le terminal.

        Exemple :
            Pikachu        PV: 35/35  [████████████████████] 100%
            Dracaufeu      PV: 20/78  [█████░░░░░░░░░░░░░░░]  26%  ⚠
        """
        barre = self._construire_barre_ascii()
        pct = self.get_pourcentage_affichage()
        etat_icon = self._get_icone_etat()

        if self._nom:
            nom_formate = f"{self._nom:<14}"
        else:
            nom_formate = ""

        print(
            f"  {nom_formate} "
            f"PV: {self._pv_actuel:>3}/{self._pv_max:<3}  "
            f"{barre}  "
            f"{pct:>3}%  "
            f"{etat_icon}"
        )

    def afficher_ko(self):
        """Affiche un message KO si les PV sont à 0."""
        if self.est_ko():
            print(f"  ✗ {self._nom} est KO !")

    def get_donnees_gui(self) -> dict:
        """
        Retourne un dictionnaire avec toutes les données nécessaires
        pour dessiner la barre dans l'interface graphique (Tkinter/Pygame).

        Returns:
            dict: Données GUI complètes.
        """
        return {
            "nom":         self._nom,
            "pv_actuel":   self._pv_actuel,
            "pv_max":      self._pv_max,
            "pourcentage": self.get_pourcentage(),
            "pct_affiche": self.get_pourcentage_affichage(),
            "couleur_hex": self.get_couleur_hex(),
            "etat":        self.get_etat(),
            "est_ko":      self.est_ko(),
        }

    # ── Mise à jour ────────────────────────────────────────────────────────────

    def appliquer_degats(self, degats: int) -> int:
        """
        Applique des dégâts et retourne les PV restants.

        Args:
            degats (int): Dégâts à infliger (>= 0).

        Returns:
            int: PV restants après les dégâts.
        """
        degats = max(0, int(degats))
        anciens_pv = self._pv_actuel
        self._pv_actuel = max(0, self._pv_actuel - degats)
        degats_reels = anciens_pv - self._pv_actuel

        if self._nom:
            print(
                f"  {self._nom} subit {degats_reels} dégâts ! "
                f"({anciens_pv} → {self._pv_actuel} PV)"
            )
        return self._pv_actuel

    def soigner(self, soin: int) -> int:
        """
        Soigne le Pokémon et retourne les PV après soin.

        Args:
            soin (int): PV à restaurer.

        Returns:
            int: PV après soin (plafonné à pv_max).
        """
        soin = max(0, int(soin))
        anciens_pv = self._pv_actuel
        self._pv_actuel = min(self._pv_max, self._pv_actuel + soin)
        soin_reel = self._pv_actuel - anciens_pv

        if self._nom and soin_reel > 0:
            print(f"  {self._nom} récupère {soin_reel} PV ! ({self._pv_actuel}/{self._pv_max})")
        return self._pv_actuel

    def reinitialiser(self):
        """Remet les PV au maximum."""
        self._pv_actuel = self._pv_max

    # ── Méthodes privées ───────────────────────────────────────────────────────

    def _construire_barre_ascii(self) -> str:
        """
        Construit la barre de progression ASCII.

        Returns:
            str: Ex. '[████████████░░░░░░░░]'
        """
        rempli = round(self.get_pourcentage() * self.LARGEUR_BARRE)
        vide = self.LARGEUR_BARRE - rempli
        return f"[{'█' * rempli}{'░' * vide}]"

    def _get_icone_etat(self) -> str:
        """Retourne une icône selon l'état des PV."""
        if self.est_ko():
            return "✗ KO"
        elif self.get_etat() == "basse":
            return "⚠ DANGER"
        elif self.get_etat() == "moyenne":
            return "!"
        return ""

    # ── Représentation ─────────────────────────────────────────────────────────

    def __repr__(self):
        return (
            f"BarreVie(nom='{self._nom}', "
            f"pv={self._pv_actuel}/{self._pv_max}, "
            f"{self.get_pourcentage_affichage()}%, "
            f"etat={self.get_etat()})"
        )

    def __str__(self):
        return (
            f"{self._nom} — {self._pv_actuel}/{self._pv_max} PV "
            f"({self.get_pourcentage_affichage()}%)"
        )


# ─── Classe BarreVieDouble ─────────────────────────────────────────────────────

class BarreVieDouble:
    """
    Affichage simultané des barres de vie des deux Pokémon en combat.
    Utilisé par l'écran de combat pour afficher les deux PV côte à côte.
    """

    def __init__(self, barre_joueur: BarreVie, barre_adverse: BarreVie):
        """
        Initialise l'affichage double.

        Args:
            barre_joueur (BarreVie): Barre du Pokémon du joueur.
            barre_adverse (BarreVie): Barre du Pokémon adverse.
        """
        self.joueur  = barre_joueur
        self.adverse = barre_adverse

    def afficher(self):
        """Affiche les deux barres de vie avec séparateur."""
        print(f"\n{'─' * 50}")
        print("  POINTS DE VIE")
        print(f"{'─' * 50}")
        self.adverse.afficher()
        self.joueur.afficher()
        print(f"{'─' * 50}\n")

    def get_donnees_gui(self) -> dict:
        """
        Retourne les données GUI pour les deux barres.

        Returns:
            dict: {'joueur': {...}, 'adverse': {...}}
        """
        return {
            "joueur":  self.joueur.get_donnees_gui(),
            "adverse": self.adverse.get_donnees_gui(),
        }

    def __repr__(self):
        return f"BarreVieDouble(joueur={self.joueur!r}, adverse={self.adverse!r})"
