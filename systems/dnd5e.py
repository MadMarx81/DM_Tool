import random
from .base import GameSystem

# Tables XP par CR
XP_PER_CR = {
    '0': 10, '1/8': 25, '1/4': 50, '1/2': 100,
    '1': 200, '2': 450, '3': 700, '4': 1100,
    '5': 1800, '6': 2300, '7': 2900, '8': 3900,
    '9': 5000, '10': 5900
}

# Seuils XP par niveau (index = niveau - 1)
XP_THRESHOLDS = [
    0, 300, 900, 2700, 6500, 14000, 23000, 34000,
    48000, 64000, 85000, 100000, 120000, 140000,
    165000, 195000, 225000, 265000, 305000, 355000
]

class DnD5eSystem(GameSystem):
    def name(self) -> str:
        return "dnd5e"

    def initiative(self, actor: dict) -> int:
        roll = random.randint(1, 20)
        return roll + actor.get('init_mod', 0)

    def xp_for_cr(self, cr: str) -> int:
        return XP_PER_CR.get(str(cr), 0)

    def compute_level(self, xp: int) -> tuple[int, int]:
        lvl = 1
        for i, req in enumerate(XP_THRESHOLDS[1:], start=2):
            if xp < req:
                break
            lvl = i
        if lvl < len(XP_THRESHOLDS):
            next_req = XP_THRESHOLDS[lvl]  # seuil pour niveau suivant
            xp_to_next = next_req - xp
        else:
            xp_to_next = 0
        return lvl, xp_to_next

    def daily_speeds(self) -> dict:
        """
        Retourne les vitesses de déplacement journalières typiques pour D&D 5e.
        En kilomètres par jour pour environ 8 heures de marche.
        """
        return {
            "marche": 24,     # 3 km/h * 8 h
            "rapide": 32,     # 4 km/h * 8 h
            "forcée": 40      # 5 km/h * 8 h, avec risques d'épuisement
        }

    def distance_units(self) -> str:
        """
        Retourne l’unité de distance utilisée dans le système.
        """
        return "feet"
