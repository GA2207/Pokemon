"""
ecran_pokedex.py - Écran Pokédex : liste scrollable, filtres par type, détail au clic
Dev 2 - Projet Pokemon - Semaine 2, Mercredi

Gère l'affichage complet du Pokédex du joueur avec :
  - Liste triée par numéro
  - Filtrage par type
  - Affichage du compteur X/1025
  - Sélection et détail d'un Pokémon
  - Pagination (scrolling terminal)
"""

from pokedex import Pokedex
from type_chart import TYPE_COLORS, TYPE_NAMES

POKEDEX_TOTAL = Pokedex.TOTAL_POKEMON

# ─── Constantes d'affichage ────────────────────────────────────────────────────

LIGNES_PAR_PAGE = 10   # Nombre de Pokémon affichés par page (scroll terminal)


class EcranPokedex:
    """
    Écran Pokédex complet avec liste scrollable, filtres et détail.

    Fournit :
      - Affichage paginé des Pokémon découverts
      - Filtrage par type (parmi les 18 types officiels)
      - Vue détaillée d'un Pokémon sélectionné
      - Compteur X/1025 permanent
      - Données prêtes pour l'interface GUI

    Attributs:
        _pokedex (Pokedex): Instance du Pokédex du joueur.
        _filtre_actif (str | None): Type actuellement filtré.
        _page_actuelle (int): Page affichée (pagination).
        _selection (dict | None): Pokémon actuellement sélectionné.
    """

    def __init__(self, pokedex: Pokedex):
        """
        Initialise l'écran Pokédex.

        Args:
            pokedex (Pokedex): Instance du Pokédex du joueur à afficher.
        """
        self._pokedex        = pokedex
        self._filtre_actif   = None
        self._page_actuelle  = 0
        self._selection      = None

    # ── Affichage principal ────────────────────────────────────────────────────

    def afficher(self):
        """
        Affiche l'écran Pokédex complet dans le terminal.
        Inclut l'en-tête, le filtre actif, la liste paginée et les contrôles.
        """
        self._afficher_entete()
        liste = self._get_liste_filtree()

        if not liste:
            self._afficher_vide()
        else:
            self._afficher_liste_paginee(liste)
            self._afficher_controles_pagination(liste)

        self._afficher_menu_actions()

    def afficher_detail(self, pokemon: dict):
        """
        Affiche la fiche détaillée d'un Pokémon sélectionné.

        Args:
            pokemon (dict): Données du Pokémon à afficher.
        """
        self._selection = pokemon
        self._afficher_fiche_pokemon(pokemon)

    # ── Filtres ────────────────────────────────────────────────────────────────

    def appliquer_filtre(self, type_pokemon: str) -> bool:
        """
        Applique un filtre par type sur la liste affichée.
        Réinitialise la pagination.

        Args:
            type_pokemon (str): Type à filtrer (ex: 'Feu').

        Returns:
            bool: True si le type est valide, False sinon.
        """
        if type_pokemon not in TYPE_NAMES:
            print(f"[Pokédex] Type inconnu : '{type_pokemon}'. Types valides : {', '.join(TYPE_NAMES)}")
            return False

        self._filtre_actif  = type_pokemon
        self._page_actuelle = 0
        nb = len(self._pokedex.filtrer_par_type(type_pokemon))
        print(f"[Pokédex] Filtre appliqué : {type_pokemon} → {nb} Pokémon trouvé(s).")
        return True

    def retirer_filtre(self):
        """Supprime le filtre actif et revient à la liste complète."""
        self._filtre_actif  = None
        self._page_actuelle = 0
        print("[Pokédex] Filtre retiré → liste complète affichée.")

    def get_filtre_actif(self) -> str | None:
        """
        Retourne le filtre de type actuellement actif.

        Returns:
            str | None: Nom du type ou None si aucun filtre.
        """
        return self._filtre_actif

    # ── Pagination ─────────────────────────────────────────────────────────────

    def page_suivante(self) -> bool:
        """
        Avance d'une page dans la liste.

        Returns:
            bool: True si la page a changé, False si déjà en dernière page.
        """
        liste = self._get_liste_filtree()
        nb_pages = self._get_nb_pages(liste)

        if self._page_actuelle < nb_pages - 1:
            self._page_actuelle += 1
            return True
        print("[Pokédex] Déjà sur la dernière page.")
        return False

    def page_precedente(self) -> bool:
        """
        Recule d'une page dans la liste.

        Returns:
            bool: True si la page a changé, False si déjà en première page.
        """
        if self._page_actuelle > 0:
            self._page_actuelle -= 1
            return True
        print("[Pokédex] Déjà sur la première page.")
        return False

    def aller_page(self, numero: int) -> bool:
        """
        Va directement à une page numérotée.

        Args:
            numero (int): Numéro de page (commence à 1 pour l'utilisateur).

        Returns:
            bool: True si la page existe et a été appliquée.
        """
        liste = self._get_liste_filtree()
        nb_pages = self._get_nb_pages(liste)
        index = numero - 1  # Conversion affichage → index

        if 0 <= index < nb_pages:
            self._page_actuelle = index
            return True
        print(f"[Pokédex] Page {numero} inexistante (1 à {nb_pages}).")
        return False

    # ── Sélection ──────────────────────────────────────────────────────────────

    def selectionner_par_nom(self, nom: str) -> dict | None:
        """
        Sélectionne un Pokémon par son nom pour afficher son détail.

        Args:
            nom (str): Nom du Pokémon (insensible à la casse).

        Returns:
            dict | None: Données du Pokémon ou None si non trouvé.
        """
        pokemon = self._pokedex.rechercher(nom)
        if pokemon:
            self._selection = pokemon
            self._afficher_fiche_pokemon(pokemon)
        else:
            print(f"[Pokédex] '{nom}' introuvable dans votre Pokédex.")
        return pokemon

    def selectionner_par_numero(self, numero: str) -> dict | None:
        """
        Sélectionne un Pokémon par son numéro de Pokédex.

        Args:
            numero (str): Numéro (ex: '025' ou '25').

        Returns:
            dict | None: Données du Pokémon ou None si non trouvé.
        """
        numero_formate = numero.zfill(3)
        liste = self._get_liste_filtree()

        for p in liste:
            if p["numero"] == numero_formate:
                self._selection = p
                self._afficher_fiche_pokemon(p)
                return p

        print(f"[Pokédex] Pokémon #{numero_formate} introuvable dans votre Pokédex.")
        return None

    # ── Données GUI ────────────────────────────────────────────────────────────

    def get_donnees_gui(self) -> dict:
        """
        Retourne toutes les données nécessaires pour l'interface graphique.

        Returns:
            dict: Données complètes pour le rendu GUI.
        """
        liste_filtree = self._get_liste_filtree()
        page_pokemon  = self._get_page_actuelle(liste_filtree)

        return {
            "compteur":        self._pokedex.get_nombre(),
            "nb_decouvert":    self._pokedex.get_nombre_int(),
            "total":           POKEDEX_TOTAL,
            "filtre_actif":    self._filtre_actif,
            "types_disponibles": self._get_types_presents(),
            "liste_filtree":   liste_filtree,
            "page_actuelle":   page_pokemon,
            "numero_page":     self._page_actuelle + 1,
            "nb_pages":        self._get_nb_pages(liste_filtree),
            "selection":       self._selection,
            "couleurs_types":  TYPE_COLORS,
        }

    # ── Méthodes privées : affichage ──────────────────────────────────────────

    def _afficher_entete(self):
        """Affiche l'en-tête du Pokédex avec compteur et filtre actif."""
        print(f"\n{'═' * 60}")
        print(f"  ★  POKÉDEX  —  {self._pokedex.get_nombre()} Pokémon découverts")
        if self._filtre_actif:
            couleur_hex = TYPE_COLORS.get(self._filtre_actif, {}).get("hex", "")
            print(f"  Filtre actif : [{self._filtre_actif}]  {couleur_hex}")
        print(f"{'═' * 60}")

    def _afficher_liste_paginee(self, liste: list):
        """
        Affiche la page actuelle de la liste filtrée.

        Args:
            liste (list): Liste complète filtrée et triée.
        """
        page = self._get_page_actuelle(liste)
        nb_pages = self._get_nb_pages(liste)

        print(f"  Page {self._page_actuelle + 1}/{nb_pages}")
        print(f"  {'#':<6} {'Nom':<16} {'Type(s)':<22} {'PV':>4} {'ATK':>4} {'DEF':>4}")
        print(f"  {'─' * 58}")

        for p in page:
            types_str = "/".join(p["types"])
            print(
                f"  #{p['numero']}  "
                f"{p['nom']:<16} "
                f"{types_str:<22} "
                f"{p['pv']:>4} "
                f"{p['attaque']:>4} "
                f"{p['defense']:>4}"
            )

    def _afficher_controles_pagination(self, liste: list):
        """Affiche les contrôles de navigation entre pages."""
        nb_pages = self._get_nb_pages(liste)
        if nb_pages > 1:
            print(f"\n  ← Page précédente  |  Page suivante →  (page {self._page_actuelle + 1}/{nb_pages})")

    def _afficher_menu_actions(self):
        """Affiche les actions disponibles dans l'écran Pokédex."""
        print(f"\n{'─' * 60}")
        print("  ACTIONS DISPONIBLES")
        print(f"{'─' * 60}")
        print("  [F] Filtrer par type      [X] Retirer le filtre")
        print("  [D] Détail d'un Pokémon   [R] Retour au menu")
        print(f"{'─' * 60}\n")

    def _afficher_vide(self):
        """Affiche un message quand la liste est vide."""
        if self._filtre_actif:
            print(f"\n  Aucun Pokémon de type [{self._filtre_actif}] dans votre Pokédex.")
        else:
            print("\n  Votre Pokédex est vide. Lancez des combats pour découvrir des Pokémon !")
        print()

    def _afficher_fiche_pokemon(self, pokemon: dict):
        """
        Affiche la fiche détaillée d'un Pokémon.

        Args:
            pokemon (dict): Données du Pokémon.
        """
        types_str = " / ".join(pokemon["types"])
        couleurs = [
            TYPE_COLORS.get(t, {}).get("hex", "#???")
            for t in pokemon["types"]
        ]
        couleurs_str = " / ".join(couleurs)

        print(f"\n{'═' * 50}")
        print(f"  ★  #{pokemon['numero']}  {pokemon['nom'].upper()}")
        print(f"{'═' * 50}")
        print(f"  Type(s)  : {types_str}")
        print(f"  Couleurs : {couleurs_str}")
        print(f"{'─' * 50}")
        print(f"  PV       : {pokemon['pv']}")
        print(f"  Attaque  : {pokemon['attaque']}")
        print(f"  Défense  : {pokemon['defense']}")
        print(f"{'═' * 50}\n")

    # ── Méthodes privées : données ─────────────────────────────────────────────

    def _get_liste_filtree(self) -> list:
        """
        Retourne la liste des Pokémon triés par numéro, avec le filtre appliqué.

        Returns:
            list: Liste triée et filtrée.
        """
        if self._filtre_actif:
            liste = self._pokedex.filtrer_par_type(self._filtre_actif)
        else:
            liste = list(self._pokedex._pokemons)

        return sorted(liste, key=lambda x: x["numero"])

    def _get_page_actuelle(self, liste: list) -> list:
        """
        Retourne uniquement les éléments de la page actuelle.

        Args:
            liste (list): Liste complète.

        Returns:
            list: Sous-liste correspondant à la page actuelle.
        """
        debut = self._page_actuelle * LIGNES_PAR_PAGE
        fin   = debut + LIGNES_PAR_PAGE
        return liste[debut:fin]

    def _get_nb_pages(self, liste: list) -> int:
        """
        Calcule le nombre total de pages.

        Args:
            liste (list): Liste complète.

        Returns:
            int: Nombre de pages (minimum 1).
        """
        if not liste:
            return 1
        return max(1, -(-len(liste) // LIGNES_PAR_PAGE))  # Division entière plafonnée

    def _get_types_presents(self) -> list:
        """
        Retourne les types présents dans le Pokédex du joueur.
        Utile pour l'interface GUI pour n'afficher que les filtres pertinents.

        Returns:
            list[str]: Types distincts présents dans le Pokédex.
        """
        types_presents = set()
        for p in self._pokedex._pokemons:
            for t in p.get("types", []):
                types_presents.add(t)
        return sorted(types_presents)

    # ── Représentation ─────────────────────────────────────────────────────────

    def __repr__(self):
        return (
            f"EcranPokedex("
            f"pokemons={self._pokedex.get_nombre()}, "
            f"filtre={self._filtre_actif!r}, "
            f"page={self._page_actuelle + 1})"
        )
