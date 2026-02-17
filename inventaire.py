"""
Module Inventaire - Gestion des objets et des Pokeballs du joueur.
"""


class Objet:
    """Represente un objet utilisable."""

    def __init__(self, nom, categorie, effet, valeur=0, condition=None):
        self.nom = nom
        self.categorie = categorie  # "soin_pv", "soin_statut", "revive", "ball"
        self.effet = effet          # Description de l'effet
        self.valeur = valeur        # Valeur numerique (PV restaures, multiplicateur ball, etc.)
        self.condition = condition  # Condition speciale (ex: type pour Filet Ball)

    def __str__(self):
        return f"{self.nom} - {self.effet}"


# =====================================================
# POKEBALLS
# =====================================================

POKE_BALL = Objet(
    "Poke Ball", "ball",
    "Pokeball standard", valeur=1.0
)

SUPER_BALL = Objet(
    "Super Ball", "ball",
    "Meilleure chance de capture (x1.5)", valeur=1.5
)

HYPER_BALL = Objet(
    "Hyper Ball", "ball",
    "Haute chance de capture (x2)", valeur=2.0
)

MASTER_BALL = Objet(
    "Master Ball", "ball",
    "Capture garantie !", valeur=255.0
)

FILET_BALL = Objet(
    "Filet Ball", "ball",
    "Efficace contre Eau/Insecte (x3.5)", valeur=3.5,
    condition={"types": ["Eau", "Insecte"], "sinon": 1.0}
)

SOMBRE_BALL = Objet(
    "Sombre Ball", "ball",
    "Efficace la nuit/en grotte (x3)", valeur=3.0,
    condition={"contexte": "nuit_grotte", "sinon": 1.0}
)

RAPIDE_BALL = Objet(
    "Rapide Ball", "ball",
    "Tres efficace au 1er tour (x5)", valeur=5.0,
    condition={"tour": 1, "sinon": 1.0}
)

TOUTES_LES_BALLS = [
    POKE_BALL, SUPER_BALL, HYPER_BALL, MASTER_BALL,
    FILET_BALL, SOMBRE_BALL, RAPIDE_BALL
]


# =====================================================
# OBJETS DE SOIN
# =====================================================

POTION = Objet("Potion", "soin_pv", "Restaure 20 PV", valeur=20)
SUPER_POTION = Objet("Super Potion", "soin_pv", "Restaure 50 PV", valeur=50)
HYPER_POTION = Objet("Hyper Potion", "soin_pv", "Restaure 200 PV", valeur=200)
POTION_MAX = Objet("Potion Max", "soin_pv", "Restaure tous les PV", valeur=-1)  # -1 = full

ANTIDOTE = Objet("Antidote", "soin_statut", "Soigne le poison", valeur=0, condition={"statut": "poison"})
ANTI_BRULE = Objet("Anti-Brule", "soin_statut", "Soigne la brulure", valeur=0, condition={"statut": "brulure"})
ANTI_PARA = Objet("Anti-Para", "soin_statut", "Soigne la paralysie", valeur=0, condition={"statut": "paralysie"})
REVEIL = Objet("Reveil", "soin_statut", "Reveille le Pokemon", valeur=0, condition={"statut": "sommeil"})
ANTIGEL = Objet("Antigel", "soin_statut", "Degivre le Pokemon", valeur=0, condition={"statut": "gel"})
TOTAL_SOIN = Objet("Total Soin", "soin_statut", "Soigne tout statut", valeur=0, condition={"statut": "tous"})

RAPPEL = Objet("Rappel", "revive", "Ranime un Pokemon KO a 50% PV", valeur=0.5)
RAPPEL_MAX = Objet("Rappel Max", "revive", "Ranime un Pokemon KO a 100% PV", valeur=1.0)

TOUS_LES_OBJETS = [
    POTION, SUPER_POTION, HYPER_POTION, POTION_MAX,
    ANTIDOTE, ANTI_BRULE, ANTI_PARA, REVEIL, ANTIGEL, TOTAL_SOIN,
    RAPPEL, RAPPEL_MAX
]


class Inventaire:
    """Gere le stock d'objets et de Pokeballs du joueur."""

    def __init__(self):
        # Stock : {nom_objet: (objet, quantite)}
        self._stock = {}

    def ajouter(self, objet, quantite=1):
        """Ajoute un objet a l'inventaire."""
        if objet.nom in self._stock:
            obj_ref, qty = self._stock[objet.nom]
            self._stock[objet.nom] = (obj_ref, qty + quantite)
        else:
            self._stock[objet.nom] = (objet, quantite)

    def retirer(self, nom_objet):
        """Retire une unite d'un objet. Retourne l'objet ou None si indisponible."""
        if nom_objet not in self._stock:
            return None
        objet, qty = self._stock[nom_objet]
        if qty <= 0:
            return None
        if qty == 1:
            del self._stock[nom_objet]
        else:
            self._stock[nom_objet] = (objet, qty - 1)
        return objet

    def get_quantite(self, nom_objet):
        """Retourne la quantite d'un objet dans l'inventaire."""
        if nom_objet in self._stock:
            return self._stock[nom_objet][1]
        return 0

    def get_balls(self):
        """Retourne la liste des Pokeballs disponibles avec leurs quantites."""
        balls = []
        for nom, (objet, qty) in self._stock.items():
            if objet.categorie == "ball" and qty > 0:
                balls.append((objet, qty))
        return balls

    def get_objets_soin(self):
        """Retourne la liste des objets de soin disponibles."""
        objets = []
        for nom, (objet, qty) in self._stock.items():
            if objet.categorie in ("soin_pv", "soin_statut", "revive") and qty > 0:
                objets.append((objet, qty))
        return objets

    def utiliser_potion(self, objet, pokemon):
        """
        Utilise une potion sur un Pokemon.
        Retourne (succes: bool, message: str).
        """
        if objet.categorie != "soin_pv":
            return False, "Cet objet n'est pas une potion."

        if pokemon.est_ko():
            return False, f"{pokemon.nom} est KO ! Utilisez un Rappel."

        if pokemon.pv >= pokemon.pv_max:
            return False, f"{pokemon.nom} a deja tous ses PV !"

        # Retirer de l'inventaire
        if not self.retirer(objet.nom):
            return False, f"Vous n'avez plus de {objet.nom} !"

        if objet.valeur == -1:
            # Potion Max : restaure tout
            pv_avant = pokemon.pv
            pokemon.pv = pokemon.pv_max
            gain = pokemon.pv - pv_avant
        else:
            pv_avant = pokemon.pv
            pokemon.pv = min(pokemon.pv_max, pokemon.pv + objet.valeur)
            gain = pokemon.pv - pv_avant

        return True, f"{pokemon.nom} recupere {gain} PV ! ({pokemon.pv}/{pokemon.pv_max})"

    def utiliser_soin_statut(self, objet, pokemon):
        """
        Utilise un soin de statut sur un Pokemon.
        Retourne (succes: bool, message: str).
        """
        if objet.categorie != "soin_statut":
            return False, "Cet objet ne soigne pas les statuts."

        if pokemon.est_ko():
            return False, f"{pokemon.nom} est KO !"

        statut_cible = objet.condition.get("statut") if objet.condition else None

        if statut_cible == "tous":
            if pokemon.statut.statut_principal is None and not pokemon.statut.confusion:
                return False, f"{pokemon.nom} n'a aucune alteration."
            if not self.retirer(objet.nom):
                return False, f"Vous n'avez plus de {objet.nom} !"
            pokemon.statut.retirer_tout()
            return True, f"{pokemon.nom} est completement soigne !"

        if statut_cible and pokemon.statut.statut_principal != statut_cible:
            return False, f"{pokemon.nom} n'est pas affecte par ce statut."

        if not self.retirer(objet.nom):
            return False, f"Vous n'avez plus de {objet.nom} !"

        pokemon.statut.retirer_statut_principal()
        return True, f"{pokemon.nom} est soigne !"

    def utiliser_rappel(self, objet, pokemon):
        """
        Utilise un Rappel sur un Pokemon KO.
        Retourne (succes: bool, message: str).
        """
        if objet.categorie != "revive":
            return False, "Cet objet n'est pas un Rappel."

        if not pokemon.est_ko():
            return False, f"{pokemon.nom} n'est pas KO !"

        if not self.retirer(objet.nom):
            return False, f"Vous n'avez plus de {objet.nom} !"

        pv_restaures = max(1, int(pokemon.pv_max * objet.valeur))
        pokemon.pv = pv_restaures
        pokemon.statut.retirer_tout()

        return True, f"{pokemon.nom} est ranime avec {pv_restaures} PV !"

    def get_multiplicateur_ball(self, ball, types_pokemon=None, tour_combat=1, contexte=None):
        """
        Calcule le multiplicateur reel d'une Pokeball selon les conditions.
        """
        if ball.valeur == 255.0:
            return 255.0  # Master Ball

        mult = ball.valeur

        if ball.condition:
            # Filet Ball : bonus si type Eau ou Insecte
            if "types" in ball.condition and types_pokemon:
                type_match = any(t in ball.condition["types"] for t in types_pokemon)
                if not type_match:
                    mult = ball.condition.get("sinon", 1.0)

            # Rapide Ball : bonus au 1er tour seulement
            elif "tour" in ball.condition:
                if tour_combat != ball.condition["tour"]:
                    mult = ball.condition.get("sinon", 1.0)

            # Sombre Ball : bonus nuit/grotte
            elif "contexte" in ball.condition:
                if contexte != ball.condition["contexte"]:
                    mult = ball.condition.get("sinon", 1.0)

        return mult

    def creer_inventaire_depart(self):
        """Remplit l'inventaire avec les objets de depart."""
        self.ajouter(POKE_BALL, 20)
        self.ajouter(SUPER_BALL, 10)
        self.ajouter(HYPER_BALL, 5)
        self.ajouter(POTION, 10)
        self.ajouter(SUPER_POTION, 5)
        self.ajouter(ANTIDOTE, 3)
        self.ajouter(ANTI_PARA, 3)
        self.ajouter(REVEIL, 3)
        self.ajouter(TOTAL_SOIN, 2)
        self.ajouter(RAPPEL, 3)

    def afficher(self):
        """Retourne une representation texte de l'inventaire."""
        if not self._stock:
            return "Inventaire vide."
        lignes = []
        lignes.append("=== POKEBALLS ===")
        for objet, qty in self.get_balls():
            lignes.append(f"  {objet.nom} x{qty}")
        lignes.append("\n=== OBJETS DE SOIN ===")
        for objet, qty in self.get_objets_soin():
            lignes.append(f"  {objet.nom} x{qty} - {objet.effet}")
        return "\n".join(lignes)

    def __str__(self):
        return self.afficher()
