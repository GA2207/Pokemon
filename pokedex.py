"""
Module Pokedex - Enregistre les Pokemon vus et captures.
Distinction entre "vu" (combattu) et "capture".
Persistance JSON.
"""

import json
import os


class Pokedex:
    """Gere le Pokedex du joueur avec distinction vu/capture."""

    TOTAL_POKEMON = 1025

    def __init__(self, chemin_json=None):
        if chemin_json is None:
            chemin_json = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "data", "pokedex.json"
            )
        self._chemin = chemin_json
        # Structure : {numero: {"nom": str, "types": list, "statut": "vu"|"capture"}}
        self._entries = {}

    def enregistrer_vu(self, pokemon):
        """
        Enregistre un Pokemon comme "vu" (combattu mais pas capture).
        Si deja capture, ne change pas le statut.
        """
        numero = pokemon.numero
        if numero in self._entries:
            # Ne pas degrader un "capture" en "vu"
            return False

        self._entries[numero] = {
            "nom": pokemon.nom,
            "types": pokemon.types,
            "statut": "vu",
        }
        return True

    def enregistrer_capture(self, pokemon):
        """
        Enregistre un Pokemon comme "capture".
        Met a jour le statut meme s'il etait deja "vu".
        """
        numero = pokemon.numero
        self._entries[numero] = {
            "nom": pokemon.nom,
            "types": pokemon.types,
            "statut": "capture",
            "pv": pokemon.pv_max,
            "attaque": pokemon.attaque,
            "defense": pokemon.defense,
            "attaque_speciale": pokemon.attaque_speciale,
            "defense_speciale": pokemon.defense_speciale,
            "vitesse": pokemon.vitesse,
        }
        return True

    def est_vu(self, numero):
        """Verifie si un Pokemon a ete vu ou capture."""
        return numero in self._entries

    def est_capture(self, numero):
        """Verifie si un Pokemon a ete capture."""
        if numero in self._entries:
            return self._entries[numero]["statut"] == "capture"
        return False

    def get_nombre_vus(self):
        """Retourne le nombre de Pokemon vus (vu + capture)."""
        return len(self._entries)

    def get_nombre_captures(self):
        """Retourne le nombre de Pokemon captures."""
        return sum(1 for e in self._entries.values() if e["statut"] == "capture")

    def get_stats(self):
        """Retourne les statistiques du Pokedex."""
        vus = self.get_nombre_vus()
        captures = self.get_nombre_captures()
        return {
            "vus": vus,
            "captures": captures,
            "total": self.TOTAL_POKEMON,
            "pourcentage_vu": round(vus / self.TOTAL_POKEMON * 100, 1),
            "pourcentage_capture": round(captures / self.TOTAL_POKEMON * 100, 1),
        }

    def filtrer_par_type(self, type_name):
        """Retourne les Pokemon du Pokedex ayant un type specifique."""
        resultats = []
        for numero, entry in sorted(self._entries.items()):
            if type_name in entry["types"]:
                resultats.append((numero, entry))
        return resultats

    def filtrer_par_statut(self, statut):
        """Retourne les Pokemon selon leur statut ('vu' ou 'capture')."""
        resultats = []
        for numero, entry in sorted(self._entries.items()):
            if entry["statut"] == statut:
                resultats.append((numero, entry))
        return resultats

    def get_entry(self, numero):
        """Retourne l'entree du Pokedex pour un numero donne."""
        return self._entries.get(numero)

    def afficher(self):
        """Retourne une representation texte du Pokedex."""
        stats = self.get_stats()
        lignes = [
            f"=== POKEDEX ===",
            f"Vus : {stats['vus']} / {stats['total']} ({stats['pourcentage_vu']}%)",
            f"Captures : {stats['captures']} / {stats['total']} ({stats['pourcentage_capture']}%)",
            f"{'=' * 40}",
        ]

        for numero, entry in sorted(self._entries.items()):
            types_str = "/".join(entry["types"])
            icone = "O" if entry["statut"] == "capture" else "-"
            lignes.append(f"  [{icone}] #{numero:04d} {entry['nom']:15s} ({types_str})")

        return "\n".join(lignes)

    def sauvegarder(self):
        """Sauvegarde le Pokedex dans un fichier JSON."""
        os.makedirs(os.path.dirname(self._chemin), exist_ok=True)

        data = {
            "stats": self.get_stats(),
            "entries": {str(k): v for k, v in self._entries.items()},
        }

        with open(self._chemin, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def charger(self):
        """Charge le Pokedex depuis un fichier JSON."""
        if not os.path.exists(self._chemin):
            return False

        try:
            with open(self._chemin, "r", encoding="utf-8") as f:
                data = json.load(f)

            self._entries = {}
            for numero_str, entry in data.get("entries", {}).items():
                self._entries[int(numero_str)] = entry
            return True
        except (json.JSONDecodeError, KeyError):
            return False

    def reinitialiser(self):
        """Remet le Pokedex a zero."""
        self._entries = {}

    def __str__(self):
        return self.afficher()

    def __len__(self):
        return len(self._entries)

    def __bool__(self):
        return True
