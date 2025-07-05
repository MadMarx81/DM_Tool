import random
from .base import GameSystem

# XP awards par CR (Starfinder Core Rulebook)
XP_PER_CR = {
    '1': 400, '2': 600, '3': 800, '4': 1200, '5': 1600,
    '6': 2400, '7': 3200, '8': 4800, '9': 6400, '10': 9600,
    '11': 12800, '12': 19200, '13': 25600, '14': 38400,
    '15': 51200, '16': 76800, '17': 102400, '18': 153600,
    '19': 204800, '20': 307200, '21': 409600, '22': 614400,
    '23': 816200, '24': 1228800, '25': 1638400,
}

# Seuils d'XP par niveau (Starfinder Player Progression)
XP_THRESHOLDS = [
    0, 1300, 3300, 6000, 10000, 15000, 23000, 34000, 50000,
    71000, 105000, 145000, 210000, 295000, 425000, 600000,
    850000, 1200000, 1700000, 2400000,
]

# Conversion entre pieds et mètres
_DISTANCE_CONVERSION = {
    'ft_to_m': 0.3048,
    'm_to_ft': 3.28084,
}

class StarfinderSystem(GameSystem):
    def name(self) -> str:
        return "starfinder"

    def initiative(self, actor: dict) -> int:
        roll = random.randint(1, 20)
        return roll + actor.get('dex_mod', actor.get('init_mod', 0))

    def xp_for_cr(self, cr: str) -> int:
        return XP_PER_CR.get(str(cr), 0)

    def compute_level(self, xp: int) -> tuple[int, int]:
        lvl = 1
        for i, req in enumerate(XP_THRESHOLDS[1:], start=2):
            if xp < req:
                break
            lvl = i
        to_next = XP_THRESHOLDS[lvl] - xp if lvl < len(XP_THRESHOLDS) else 0
        return lvl, to_next

    def distance_units(self) -> str:
        """Unité de base de déplacement (par défaut en pieds)."""
        return "ft"

    def convert_distance(self, value: float, from_unit: str, to_unit: str) -> float:
        """
        Convertit une distance entre pieds et mètres.
        Ex : convert_distance(30, 'ft', 'm') -> ~9.144
        """
        key = f"{from_unit}_to_{to_unit}"
        factor = _DISTANCE_CONVERSION.get(key)
        return value * factor if factor else value

    def default_speed(self, actor: dict) -> float:
        """
        Récupère la vitesse de l’acteur en pieds par round.
        Accepte dict de vitesses (ex: {'walk': 30}) ou int direct.
        """
        speeds = actor.get('speed', {})
        if isinstance(speeds, dict):
            return speeds.get('walk', 0)
        return float(speeds or 0)

    def daily_speeds(self) -> dict:
        """
        Retourne des vitesses de déplacement journalières standards (en km/jour).
        Adaptées pour un environnement de type terrestre.
        """
        return {
            "marche": 48,     # 6 km/h * 8 h
            "rapide": 64,     # 8 km/h * 8 h
            "forcée": 80      # 10 km/h * 8 h, avec fatigue
        }
