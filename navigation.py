"""
navigation.py - Gestionnaire de navigation entre les écrans du jeu
Dev 2 - Projet Pokemon - Semaine 2, Lundi

Gère la pile d'écrans (stack), les transitions, et l'historique de navigation.
"""

from enum import Enum


# ─── Écrans disponibles ────────────────────────────────────────────────────────

class Ecran(Enum):
    """
    Enumération des écrans disponibles dans l'application.
    Permet une navigation typée et sans erreurs de frappe.
    """
    MENU_PRINCIPAL   = "menu_principal"
    SELECTION_POKEMON = "selection_pokemon"
    COMBAT           = "combat"
    POKEDEX          = "pokedex"
    DETAIL_POKEMON   = "detail_pokemon"
    AJOUTER_POKEMON  = "ajouter_pokemon"
    VICTOIRE         = "victoire"
    DEFAITE          = "defaite"


# ─── Classe Navigation ─────────────────────────────────────────────────────────

class Navigation:
    """
    Gestionnaire de navigation par pile (stack).

    Permet de naviguer entre les écrans avec un historique,
    de revenir en arrière, et de passer des données entre écrans.

    Exemple d'utilisation :
        nav = Navigation()
        nav.aller_a(Ecran.SELECTION_POKEMON)
        nav.aller_a(Ecran.COMBAT, {"pokemon_joueur": pikachu, "pokemon_adverse": dracaufeu})
        nav.retour()  # → SELECTION_POKEMON
    """

    def __init__(self, ecran_initial: Ecran = Ecran.MENU_PRINCIPAL):
        """
        Initialise la navigation avec l'écran de départ.

        Args:
            ecran_initial (Ecran): Écran affiché au lancement.
        """
        self._pile: list[tuple[Ecran, dict]] = [(ecran_initial, {})]
        self._callbacks: dict[Ecran, callable] = {}
        self._callback_changement: callable = None

    # ── Navigation principale ──────────────────────────────────────────────────

    def aller_a(self, ecran: Ecran, donnees: dict = None):
        """
        Navigue vers un nouvel écran en empilant l'écran actuel.

        Args:
            ecran (Ecran): Écran de destination.
            donnees (dict): Données à transmettre à l'écran (optionnel).
        """
        donnees = donnees or {}
        self._pile.append((ecran, donnees))
        print(f"[Navigation] → {ecran.value}  (pile : {self._get_noms_pile()})")
        self._notifier_changement(ecran, donnees)

    def retour(self) -> bool:
        """
        Revient à l'écran précédent (dépile).

        Returns:
            bool: True si retour effectué, False si déjà sur l'écran racine.
        """
        if len(self._pile) <= 1:
            print("[Navigation] Impossible de revenir en arrière : écran racine.")
            return False

        self._pile.pop()
        ecran_actuel, donnees = self._pile[-1]
        print(f"[Navigation] ← Retour vers {ecran_actuel.value}  (pile : {self._get_noms_pile()})")
        self._notifier_changement(ecran_actuel, donnees)
        return True

    def remplacer(self, ecran: Ecran, donnees: dict = None):
        """
        Remplace l'écran actuel sans l'empiler (pas de retour possible).
        Utile pour les transitions définitives (ex : menu → sélection).

        Args:
            ecran (Ecran): Écran de remplacement.
            donnees (dict): Données à transmettre (optionnel).
        """
        donnees = donnees or {}
        if self._pile:
            self._pile[-1] = (ecran, donnees)
        else:
            self._pile.append((ecran, donnees))
        print(f"[Navigation] ⇄ Remplacement par {ecran.value}  (pile : {self._get_noms_pile()})")
        self._notifier_changement(ecran, donnees)

    def reset(self, ecran: Ecran = Ecran.MENU_PRINCIPAL):
        """
        Réinitialise la navigation et revient à l'écran racine.

        Args:
            ecran (Ecran): Écran de départ (par défaut : MENU_PRINCIPAL).
        """
        self._pile = [(ecran, {})]
        print(f"[Navigation] ↺ Reset → {ecran.value}")
        self._notifier_changement(ecran, {})

    # ── Accesseurs ─────────────────────────────────────────────────────────────

    def get_ecran_actuel(self) -> Ecran:
        """
        Retourne l'écran actuellement affiché.

        Returns:
            Ecran: Écran en haut de la pile.
        """
        return self._pile[-1][0]

    def get_donnees_actuelles(self) -> dict:
        """
        Retourne les données associées à l'écran actuel.

        Returns:
            dict: Données transmises lors de la navigation.
        """
        return self._pile[-1][1]

    def get_historique(self) -> list[Ecran]:
        """
        Retourne la liste ordonnée des écrans dans la pile.

        Returns:
            list[Ecran]: Du premier au dernier écran visité.
        """
        return [ecran for ecran, _ in self._pile]

    def peut_revenir(self) -> bool:
        """
        Indique si un retour en arrière est possible.

        Returns:
            bool: True si la pile contient plus d'un écran.
        """
        return len(self._pile) > 1

    def est_sur(self, ecran: Ecran) -> bool:
        """
        Vérifie si l'écran actuel correspond à l'écran donné.

        Args:
            ecran (Ecran): Écran à vérifier.

        Returns:
            bool: True si l'écran actuel correspond.
        """
        return self.get_ecran_actuel() == ecran

    # ── Callbacks ──────────────────────────────────────────────────────────────

    def enregistrer_callback(self, ecran: Ecran, callback: callable):
        """
        Enregistre une fonction à appeler lors de la navigation vers un écran.

        Args:
            ecran (Ecran): Écran déclencheur.
            callback (callable): Fonction appelée avec (ecran, donnees).
        """
        self._callbacks[ecran] = callback

    def enregistrer_callback_global(self, callback: callable):
        """
        Enregistre une fonction appelée à chaque changement d'écran.
        Utilisée par l'interface graphique pour mettre à jour l'affichage.

        Args:
            callback (callable): Fonction appelée avec (ecran, donnees).
        """
        self._callback_changement = callback

    # ── Méthodes privées ───────────────────────────────────────────────────────

    def _notifier_changement(self, ecran: Ecran, donnees: dict):
        """
        Notifie les callbacks enregistrés lors d'un changement d'écran.

        Args:
            ecran (Ecran): Nouvel écran actif.
            donnees (dict): Données associées.
        """
        # Callback spécifique à l'écran
        if ecran in self._callbacks:
            self._callbacks[ecran](ecran, donnees)

        # Callback global (interface graphique)
        if self._callback_changement:
            self._callback_changement(ecran, donnees)

    def _get_noms_pile(self) -> str:
        """Retourne la pile sous forme lisible pour les logs."""
        return " > ".join(e.value for e, _ in self._pile)

    # ── Représentation ─────────────────────────────────────────────────────────

    def __repr__(self):
        return f"Navigation(actuel={self.get_ecran_actuel().value}, profondeur={len(self._pile)})"

    def __str__(self):
        return f"Écran actuel : {self.get_ecran_actuel().value} | Historique : {self._get_noms_pile()}"
