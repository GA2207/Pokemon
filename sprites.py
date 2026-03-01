"""
sprites.py - Gestion des sprites et assets visuels des Pokémon
Dev 2 - Projet Pokemon - Semaine 2, Jeudi

Gère le chargement, la mise en cache et l'affichage des sprites Pokémon.
Fournit des sprites ASCII de fallback si les images sont absentes.
Compatible Tkinter et Pygame selon la configuration du projet.
"""

import os
from type_chart import TYPE_COLORS


# ─── Constantes ────────────────────────────────────────────────────────────────

DOSSIER_SPRITES = os.path.join("assets", "sprites")
EXTENSIONS_VALIDES = (".png", ".gif", ".jpg", ".jpeg")

# Tailles standards des sprites
TAILLE_COMBAT_JOUEUR  = (150, 150)   # Sprite joueur (plus grand, en bas)
TAILLE_COMBAT_ADVERSE = (120, 120)   # Sprite adverse (plus petit, en haut)
TAILLE_POKEDEX        = (64, 64)     # Miniature dans la liste Pokédex


# ─── Sprites ASCII de substitution ────────────────────────────────────────────
# Utilisés si les vraies images sont absentes (mode terminal ou test)

SPRITES_ASCII = {
    # Starters
    "001": ["  █▄▄█  ", " ▐█▓▓█▌ ", "  ████  ", " ██████ ", "  ████  "],  # Bulbizarre
    "004": [" ▐█▄▄█▌ ", "  ████  ", " ▐████▌ ", "  ▀██▀  ", "   ▄▄   "],  # Salameche
    "007": ["  ████  ", " ██████ ", "▐██████▌", " ██████ ", "  ████  "],  # Carapuce
    "025": [" /\\  /\\ ", "(  oo  )", " \\    / ", "  \\  /  ", "  /  \\  "],  # Pikachu
    "006": [" █▄  ▄█ ", "  ████  ", " ██████ ", "  ▀██▀  ", "  /  \\  "],  # Dracaufeu
    "009": ["  ████  ", " ██████ ", "▐██████▌", " ██▄▄██ ", "  ████  "],  # Tortank
    "150": [" ██████ ", "█▐████▌█", "█▐████▌█", " ██████ ", "  █  █  "],  # Mewtwo
    "151": ["   ██   ", "  ████  ", " ██████ ", "  ████  ", "   ██   "],  # Mew
}

SPRITE_DEFAUT = [
    " ╔════╗ ",
    " ║ ?? ║ ",
    " ║    ║ ",
    " ╚════╝ ",
    "   ██   ",
]


# ─── Classe SpriteManager ─────────────────────────────────────────────────────

class SpriteManager:
    """
    Gestionnaire centralisé des sprites et assets visuels Pokémon.

    Fonctionnalités :
      - Chargement des images depuis assets/sprites/
      - Cache pour éviter les rechargements inutiles
      - Redimensionnement selon le contexte (combat / Pokédex)
      - Sprite ASCII de substitution si l'image est absente
      - Badge de type coloré (hex)

    Attributs:
        _cache (dict): Cache des images chargées {chemin: image}.
        _dossier (str): Chemin du dossier de sprites.
        _mode_gui (str): 'tkinter', 'pygame', ou 'terminal'.
    """

    def __init__(self, dossier: str = DOSSIER_SPRITES, mode_gui: str = "terminal"):
        """
        Initialise le gestionnaire de sprites.

        Args:
            dossier (str): Chemin vers le dossier contenant les sprites PNG.
            mode_gui (str): Mode d'affichage ('tkinter', 'pygame', 'terminal').
        """
        self._dossier  = dossier
        self._cache    = {}
        self._mode_gui = mode_gui

        self._verifier_dossier()

    # ── Chargement d'images ────────────────────────────────────────────────────

    def get_sprite(self, numero: str, taille: tuple = None):
        """
        Retourne le sprite d'un Pokémon (image ou ASCII selon disponibilité).

        En mode terminal : retourne le sprite ASCII.
        En mode GUI : retourne l'objet image chargé (Tkinter/Pygame).

        Args:
            numero (str): Numéro du Pokémon (ex: '025').
            taille (tuple): Taille souhaitée (largeur, hauteur). None = taille originale.

        Returns:
            Image | list[str] | None: Objet image ou sprite ASCII.
        """
        numero = numero.zfill(3)

        if self._mode_gui == "terminal":
            return self.get_sprite_ascii(numero)

        chemin = self._trouver_chemin_sprite(numero)

        if not chemin:
            print(f"[Sprites] Sprite introuvable pour #{numero} → ASCII utilisé.")
            return self.get_sprite_ascii(numero)

        return self._charger_image(chemin, taille)

    def get_sprite_combat_joueur(self, numero: str):
        """
        Retourne le sprite taille combat pour le Pokémon du joueur.

        Args:
            numero (str): Numéro du Pokémon.

        Returns:
            Image | list[str]: Sprite redimensionné ou ASCII.
        """
        return self.get_sprite(numero, taille=TAILLE_COMBAT_JOUEUR)

    def get_sprite_combat_adverse(self, numero: str):
        """
        Retourne le sprite taille combat pour le Pokémon adverse.

        Args:
            numero (str): Numéro du Pokémon.

        Returns:
            Image | list[str]: Sprite redimensionné ou ASCII.
        """
        return self.get_sprite(numero, taille=TAILLE_COMBAT_ADVERSE)

    def get_sprite_pokedex(self, numero: str):
        """
        Retourne la miniature pour l'écran Pokédex.

        Args:
            numero (str): Numéro du Pokémon.

        Returns:
            Image | list[str]: Miniature ou ASCII.
        """
        return self.get_sprite(numero, taille=TAILLE_POKEDEX)

    # ── Sprites ASCII ──────────────────────────────────────────────────────────

    def get_sprite_ascii(self, numero: str) -> list[str]:
        """
        Retourne le sprite ASCII d'un Pokémon.
        Utilise le sprite personnalisé s'il existe, sinon le sprite par défaut.

        Args:
            numero (str): Numéro du Pokémon (ex: '025').

        Returns:
            list[str]: Liste de lignes formant le sprite ASCII.
        """
        numero = numero.zfill(3)
        return SPRITES_ASCII.get(numero, SPRITE_DEFAUT)

    def afficher_sprite_ascii(self, numero: str, nom: str = "", aligner_droite: bool = False):
        """
        Affiche un sprite ASCII dans le terminal.

        Args:
            numero (str): Numéro du Pokémon.
            nom (str): Nom à afficher sous le sprite.
            aligner_droite (bool): Si True, décale le sprite à droite (Pokémon adverse).
        """
        sprite = self.get_sprite_ascii(numero)
        indent = "          " if aligner_droite else "  "

        for ligne in sprite:
            print(f"{indent}{ligne}")

        if nom:
            centre = nom.center(len(sprite[0]))
            print(f"{indent}{centre}")

    def afficher_combat_ascii(self, pokemon_joueur: dict, pokemon_adverse: dict):
        """
        Affiche les deux sprites côte à côte pour l'écran de combat.

        Args:
            pokemon_joueur (dict): Données du Pokémon du joueur.
            pokemon_adverse (dict): Données du Pokémon adverse.
        """
        sprite_j = self.get_sprite_ascii(pokemon_joueur["numero"])
        sprite_a = self.get_sprite_ascii(pokemon_adverse["numero"])

        print(f"\n{'═' * 50}")

        # Adverse à droite, joueur à gauche
        max_lignes = max(len(sprite_j), len(sprite_a))

        for i in range(max_lignes):
            ligne_j = sprite_j[i] if i < len(sprite_j) else " " * 9
            ligne_a = sprite_a[i] if i < len(sprite_a) else " " * 9
            print(f"  {ligne_j}           {ligne_a}")

        # Noms sous les sprites
        nom_j = pokemon_joueur["nom"].center(9)
        nom_a = pokemon_adverse["nom"].center(9)
        print(f"  {nom_j}           {nom_a}")
        print(f"{'═' * 50}\n")

    # ── Badges de type ─────────────────────────────────────────────────────────

    def get_badge_type(self, type_nom: str) -> dict:
        """
        Retourne les données d'un badge de type coloré.
        Utilisé par l'interface GUI pour afficher des badges visuels.

        Args:
            type_nom (str): Nom du type (ex: 'Feu').

        Returns:
            dict: {'nom': str, 'hex': str, 'rgb': tuple}
        """
        couleurs = TYPE_COLORS.get(type_nom, {"hex": "#FFFFFF", "rgb": (255, 255, 255)})
        return {
            "nom": type_nom,
            "hex": couleurs.get("hex", "#FFFFFF"),
            "rgb": couleurs.get("rgb", (255, 255, 255)),
        }

    def get_badges_types(self, types: list[str]) -> list[dict]:
        """
        Retourne la liste des badges pour tous les types d'un Pokémon.

        Args:
            types (list[str]): Liste de 1 ou 2 types.

        Returns:
            list[dict]: Liste de badges avec couleurs.
        """
        return [self.get_badge_type(t) for t in types]

    def afficher_badges_ascii(self, types: list[str]):
        """
        Affiche les badges de type en ASCII dans le terminal.

        Args:
            types (list[str]): Liste de types à afficher.
        """
        badges = []
        for t in types:
            hex_color = TYPE_COLORS.get(t, {}).get("hex", "#???")
            badges.append(f"[{t}] {hex_color}")
        print("  Types : " + "  |  ".join(badges))

    # ── Inventaire des sprites ─────────────────────────────────────────────────

    def lister_sprites_disponibles(self) -> list[str]:
        """
        Retourne la liste des numéros de Pokémon dont le sprite est disponible.

        Returns:
            list[str]: Numéros disponibles (ex: ['001', '004', '007']).
        """
        if not os.path.exists(self._dossier):
            return []

        disponibles = []
        for fichier in os.listdir(self._dossier):
            nom, ext = os.path.splitext(fichier)
            if ext.lower() in EXTENSIONS_VALIDES:
                disponibles.append(nom.zfill(3))

        return sorted(disponibles)

    def get_stats_sprites(self) -> dict:
        """
        Retourne des statistiques sur les sprites disponibles.

        Returns:
            dict: Nombre de sprites disponibles, manquants, et pourcentage.
        """
        disponibles = self.lister_sprites_disponibles()
        nb_disponibles = len(disponibles)
        nb_total = 151
        nb_manquants = nb_total - nb_disponibles
        pct = round(nb_disponibles / nb_total * 100, 1)

        return {
            "disponibles": nb_disponibles,
            "manquants":   nb_manquants,
            "total":       nb_total,
            "pourcentage": pct,
            "numeros":     disponibles,
        }

    def afficher_stats_sprites(self):
        """Affiche les statistiques de sprites dans le terminal."""
        stats = self.get_stats_sprites()
        print(f"\n[Sprites] {stats['disponibles']}/{stats['total']} sprites disponibles "
              f"({stats['pourcentage']}%)")
        if stats["manquants"] > 0:
            print(f"[Sprites] {stats['manquants']} sprites manquants → fallback ASCII actif.")

    # ── Vider le cache ─────────────────────────────────────────────────────────

    def vider_cache(self):
        """Vide le cache des images chargées (libère la mémoire)."""
        nb = len(self._cache)
        self._cache.clear()
        print(f"[Sprites] Cache vidé ({nb} image(s) libérée(s)).")

    # ── Méthodes privées ───────────────────────────────────────────────────────

    def _verifier_dossier(self):
        """Vérifie que le dossier de sprites existe et affiche un avertissement sinon."""
        if not os.path.exists(self._dossier):
            print(
                f"[Sprites] Dossier '{self._dossier}' introuvable. "
                f"Sprites ASCII activés pour tous les Pokémon."
            )

    def _trouver_chemin_sprite(self, numero: str) -> str | None:
        """
        Cherche le fichier sprite d'un Pokémon parmi les extensions valides.

        Args:
            numero (str): Numéro du Pokémon (format '025').

        Returns:
            str | None: Chemin complet du fichier ou None si absent.
        """
        for ext in EXTENSIONS_VALIDES:
            chemin = os.path.join(self._dossier, f"{numero}{ext}")
            if os.path.exists(chemin):
                return chemin
        return None

    def _charger_image(self, chemin: str, taille: tuple = None):
        """
        Charge une image depuis le disque avec mise en cache.
        Compatible Tkinter et Pygame selon le mode configuré.

        Args:
            chemin (str): Chemin complet vers le fichier image.
            taille (tuple | None): Taille souhaitée (w, h) ou None.

        Returns:
            Image | None: Objet image ou None si échec du chargement.
        """
        cle_cache = f"{chemin}_{taille}"

        if cle_cache in self._cache:
            return self._cache[cle_cache]

        try:
            if self._mode_gui == "tkinter":
                image = self._charger_tkinter(chemin, taille)
            elif self._mode_gui == "pygame":
                image = self._charger_pygame(chemin, taille)
            else:
                image = None

            self._cache[cle_cache] = image
            return image

        except Exception as e:
            print(f"[Sprites] Erreur chargement '{chemin}' : {e} → ASCII utilisé.")
            return None

    def _charger_tkinter(self, chemin: str, taille: tuple = None):
        """
        Charge une image pour Tkinter (PhotoImage ou PIL).

        Args:
            chemin (str): Chemin du fichier image.
            taille (tuple | None): Taille souhaitée.

        Returns:
            PhotoImage | ImageTk.PhotoImage: Image Tkinter.
        """
        try:
            from PIL import Image, ImageTk
            img = Image.open(chemin).convert("RGBA")
            if taille:
                img = img.resize(taille, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except ImportError:
            # Fallback sans PIL : Tkinter natif (PNG uniquement)
            import tkinter as tk
            photo = tk.PhotoImage(file=chemin)
            if taille:
                # Tkinter natif ne supporte pas le resize facilement
                pass
            return photo

    def _charger_pygame(self, chemin: str, taille: tuple = None):
        """
        Charge une image pour Pygame (Surface).

        Args:
            chemin (str): Chemin du fichier image.
            taille (tuple | None): Taille souhaitée.

        Returns:
            pygame.Surface: Surface Pygame.
        """
        import pygame
        surface = pygame.image.load(chemin).convert_alpha()
        if taille:
            surface = pygame.transform.scale(surface, taille)
        return surface

    # ── Représentation ─────────────────────────────────────────────────────────

    def __repr__(self):
        stats = self.get_stats_sprites()
        return (
            f"SpriteManager("
            f"mode={self._mode_gui}, "
            f"sprites={stats['disponibles']}/{stats['total']}, "
            f"cache={len(self._cache)} entrée(s))"
        )
