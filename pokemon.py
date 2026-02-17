"""
Module Pokemon - Classe de base pour tous les Pokemon.
Gere les stats, statuts, XP, evolution et interactions de combat.
"""

import json
import os
import random

from statut import Statut
from experience import Experience
from type_chart import TypeChart


class Pokemon:
    """Represente un Pokemon avec toutes ses caracteristiques."""

    def __init__(self, numero, nom, types, pv, attaque, defense,
                 attaque_speciale, defense_speciale, vitesse,
                 niveau=5, base_xp=64, taux_capture=45,
                 evolution_id=None, evolution_niveau=None, evolution_nom=None):
        # Identite
        self.numero = numero
        self.nom = nom
        self.types = types if isinstance(types, list) else [types]

        # Stats de base (pour recalcul au level up)
        self._stats_base = {
            "pv": pv,
            "attaque": attaque,
            "defense": defense,
            "attaque_speciale": attaque_speciale,
            "defense_speciale": defense_speciale,
            "vitesse": vitesse,
        }

        # Stats actuelles (calculees en fonction du niveau)
        self.niveau = niveau
        stats = Experience.calculer_nouvelles_stats(self._stats_base, 1, niveau)
        self.pv_max = stats["pv"]
        self.pv = self.pv_max
        self.attaque = stats["attaque"]
        self.defense = stats["defense"]
        self.attaque_speciale = stats["attaque_speciale"]
        self.defense_speciale = stats["defense_speciale"]
        self.vitesse = stats["vitesse"]

        # Experience
        self.base_xp = base_xp
        self.xp = Experience.xp_pour_niveau(niveau)

        # Capture
        self.taux_capture = taux_capture

        # Evolution
        self.evolution_id = evolution_id
        self.evolution_niveau = evolution_niveau
        self.evolution_nom = evolution_nom

        # Statut
        self.statut = Statut()

    def attaquer(self, adversaire, est_special=False):
        """
        Attaque un adversaire.
        Retourne (degats: int, messages: list[str]).
        """
        messages = []

        # Verifier si le Pokemon peut agir (statuts)
        peut_agir, msg_statut = self.statut.peut_agir()
        if msg_statut:
            messages.append(msg_statut)

        if not peut_agir:
            if msg_statut == "CONFUSION":
                # Le Pokemon se frappe lui-meme
                degats_confusion = max(1, self.attaque // 4)
                self.subir_degats(degats_confusion)
                messages.append(f"{self.nom} se blesse dans sa confusion ! (-{degats_confusion} PV)")
                return 0, messages
            return 0, messages

        # Calcul des degats
        if est_special:
            att_stat = self.attaque_speciale
            def_stat = adversaire.defense_speciale
        else:
            att_stat = self.attaque
            def_stat = adversaire.defense

        # Modificateur de brulure sur attaque physique
        if not est_special:
            att_stat = int(att_stat * self.statut.get_modificateur_attaque())

        # Multiplicateur de type (STAB + efficacite)
        mult_type = 1.0
        for type_att in self.types:
            m = TypeChart.get_multiplicateur(type_att, adversaire.types)
            if m != 1.0:
                mult_type = m
                break  # On prend le premier type qui a un effet

        # STAB (Same Type Attack Bonus)
        stab = 1.0
        # Simplification : on considere que l'attaque est du premier type du Pokemon
        # Le STAB s'applique si le type de l'attaque = un des types du Pokemon
        stab = 1.5  # On applique le STAB par defaut (l'attaque est du type du Pokemon)

        # Coup critique (4.17% de chance)
        critique = False
        if random.random() < (1 / 24):
            critique = True
            messages.append("Coup critique !")

        mult_critique = 1.5 if critique else 1.0

        # Random factor (0.85 - 1.0)
        random_factor = random.uniform(0.85, 1.0)

        # Formule de degats
        puissance = 80  # Puissance de base d'une attaque standard
        degats_bruts = ((2 * self.niveau / 5 + 2) * puissance * att_stat / def_stat / 50 + 2)
        degats_bruts *= mult_type * stab * mult_critique * random_factor

        degats = max(1, int(degats_bruts))

        # Message d'efficacite
        msg_eff = TypeChart.get_message_efficacite(mult_type)
        if msg_eff:
            messages.append(msg_eff)

        # Appliquer les degats
        adversaire.subir_degats(degats)
        messages.append(f"{self.nom} inflige {degats} degats a {adversaire.nom} !")

        if adversaire.est_ko():
            messages.append(f"{adversaire.nom} est KO !")

        return degats, messages

    def subir_degats(self, degats):
        """Reduit les PV du Pokemon."""
        self.pv = max(0, self.pv - degats)

    def soigner(self, montant):
        """Restaure des PV."""
        self.pv = min(self.pv_max, self.pv + montant)

    def est_ko(self):
        """Retourne True si le Pokemon est KO (PV = 0)."""
        return self.pv <= 0

    def get_vitesse_effective(self):
        """Retourne la vitesse effective (avec modificateur de paralysie)."""
        return int(self.vitesse * self.statut.get_modificateur_vitesse())

    def gagner_xp(self, montant):
        """
        Ajoute de l'XP et gere les montees de niveau.
        Retourne une liste de messages.
        """
        messages = []
        self.xp += montant
        messages.append(f"{self.nom} gagne {montant} points d'experience !")

        ancien_niveau = self.niveau
        nouveau_niveau = Experience.calculer_niveaux_gagnes(self.xp, self.niveau)

        if nouveau_niveau > ancien_niveau:
            self.niveau = nouveau_niveau
            self._recalculer_stats()
            messages.append(f"{self.nom} monte au niveau {self.niveau} !")

            # Verifier evolution
            if self.peut_evoluer():
                messages.append(f"{self.nom} peut evoluer en {self.evolution_nom} !")

        return messages

    def _recalculer_stats(self):
        """Recalcule les stats en fonction du niveau actuel."""
        stats = Experience.calculer_nouvelles_stats(self._stats_base, 1, self.niveau)
        ancien_pv_max = self.pv_max
        self.pv_max = stats["pv"]
        self.attaque = stats["attaque"]
        self.defense = stats["defense"]
        self.attaque_speciale = stats["attaque_speciale"]
        self.defense_speciale = stats["defense_speciale"]
        self.vitesse = stats["vitesse"]
        # Ajuster les PV actuels proportionnellement
        self.pv = min(self.pv_max, self.pv + (self.pv_max - ancien_pv_max))

    def peut_evoluer(self):
        """Verifie si le Pokemon peut evoluer."""
        if self.evolution_id is None or self.evolution_nom is None:
            return False
        if self.evolution_niveau is not None:
            return self.niveau >= self.evolution_niveau
        return False

    def evoluer(self, donnees_pokemon):
        """
        Fait evoluer le Pokemon.

        Args:
            donnees_pokemon: dict des donnees du Pokemon evolue (depuis pokemon.json)

        Retourne (succes: bool, message: str).
        """
        if not self.peut_evoluer():
            return False, f"{self.nom} ne peut pas evoluer."

        ancien_nom = self.nom

        # Mettre a jour les infos
        self.numero = donnees_pokemon["numero"]
        self.nom = donnees_pokemon["nom"]
        self.types = donnees_pokemon["types"]
        self._stats_base = {
            "pv": donnees_pokemon["pv"],
            "attaque": donnees_pokemon["attaque"],
            "defense": donnees_pokemon["defense"],
            "attaque_speciale": donnees_pokemon["attaque_speciale"],
            "defense_speciale": donnees_pokemon["defense_speciale"],
            "vitesse": donnees_pokemon["vitesse"],
        }
        self.base_xp = donnees_pokemon["base_xp"]
        self.taux_capture = donnees_pokemon["taux_capture"]
        self.evolution_id = donnees_pokemon.get("evolution_id")
        self.evolution_niveau = donnees_pokemon.get("evolution_niveau")
        self.evolution_nom = donnees_pokemon.get("evolution_nom")

        # Recalculer les stats
        self._recalculer_stats()
        self.pv = self.pv_max  # Full PV apres evolution

        return True, f"{ancien_nom} evolue en {self.nom} !"

    def get_pourcentage_pv(self):
        """Retourne le pourcentage de PV restants."""
        if self.pv_max <= 0:
            return 0
        return int((self.pv / self.pv_max) * 100)

    def to_dict(self):
        """Convertit le Pokemon en dictionnaire (pour sauvegarde JSON)."""
        return {
            "numero": self.numero,
            "nom": self.nom,
            "types": self.types,
            "niveau": self.niveau,
            "pv": self.pv,
            "pv_max": self.pv_max,
            "attaque": self.attaque,
            "defense": self.defense,
            "attaque_speciale": self.attaque_speciale,
            "defense_speciale": self.defense_speciale,
            "vitesse": self.vitesse,
            "xp": self.xp,
            "base_xp": self.base_xp,
            "taux_capture": self.taux_capture,
            "evolution_id": self.evolution_id,
            "evolution_niveau": self.evolution_niveau,
            "evolution_nom": self.evolution_nom,
        }

    def __str__(self):
        types_str = "/".join(self.types)
        statut_str = f" [{self.statut}]" if self.statut.statut_principal or self.statut.confusion else ""
        return (
            f"#{self.numero:04d} {self.nom} ({types_str}) Niv.{self.niveau}\n"
            f"  PV: {self.pv}/{self.pv_max} | ATK: {self.attaque} | DEF: {self.defense}\n"
            f"  ATK Spe: {self.attaque_speciale} | DEF Spe: {self.defense_speciale} | VIT: {self.vitesse}"
            f"{statut_str}"
        )

    @staticmethod
    def depuis_json(donnees, niveau=None):
        """
        Cree un Pokemon depuis un dictionnaire JSON (pokemon.json).
        """
        niv = niveau if niveau else random.randint(3, 10)
        return Pokemon(
            numero=donnees["numero"],
            nom=donnees["nom"],
            types=donnees["types"],
            pv=donnees["pv"],
            attaque=donnees["attaque"],
            defense=donnees["defense"],
            attaque_speciale=donnees["attaque_speciale"],
            defense_speciale=donnees["defense_speciale"],
            vitesse=donnees["vitesse"],
            niveau=niv,
            base_xp=donnees.get("base_xp", 64),
            taux_capture=donnees.get("taux_capture", 45),
            evolution_id=donnees.get("evolution_id"),
            evolution_niveau=donnees.get("evolution_niveau"),
            evolution_nom=donnees.get("evolution_nom"),
        )

    @staticmethod
    def charger_tous(chemin_json=None):
        """Charge tous les Pokemon depuis le fichier pokemon.json."""
        if chemin_json is None:
            chemin_json = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "data", "pokemon.json"
            )
        with open(chemin_json, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data["pokemons"]
