import random
from .base import GameSystem

# À adapter / remplir avec les valeurs officielles Starfinder
# XP awards par CR (à vérifier dans le Starfinder Core Rulebook)
XP_PER_CR = {
    '1': 400,
    '2': 600,
    '3': 800,
    '4': 1200,
    '5': 1600,
    '6': 2400,
    '7': 3200,
    '8': 4800,
    '9': 6400,
    '10': 9600,
    '11': 12800,
    '12': 19200,
    '13': 25600,
    '14': 38400,
    '15': 51200,
    '16': 76800,
    '17': 102400,
    '18': 153600,
    '19': 204800,
    '20': 307200,
    '21': 409600,
    '22': 614400,
    '23': 816200,
    '24': 1228800,
    '25': 1638400,
    # …
}

# Seuils d'XP par niveau (Level 1 → 0 xp, Level 2 → X xp, …)
# À adapter selon la table Starfinder
XP_THRESHOLDS = [
    0,    # level 1
    1300, # level 2
    3300, # level 3
    6000, # level 4
    10000,# level 5
    15000,# level 6
    23000,# level 7
    34000,# level 8
    50000,# level 9
    71000,# level 10
    105000,# level 11
    145000,# level 12
    210000,# level 13
    295000,# level 14
    425000,# level 15
    600000,# level 16
    850000,# level 17
    1200000,# level 18
    1700000,# level 19
    2400000,# level 20
    # …
]

class StarfinderSystem(GameSystem):
    def name(self) -> str:
        return "starfinder"

    def initiative(self, actor: dict) -> int:
        """
        Jet d’initiative SF : 1d20 + bonus de Dex ou mod de classe.
        On cherche dans actor['dex_mod'] ou actor['init_mod'], à adapter.
        """
        roll = random.randint(1, 20)
        return roll + actor.get('dex_mod', actor.get('init_mod', 0))

    def xp_for_cr(self, cr: str) -> int:
        # Retourne l’XP à distribuer pour une créature de CR donné
        return XP_PER_CR.get(str(cr), 0)

    def compute_level(self, xp: int) -> tuple[int, int]:
        """
        Renvoie (niveau_courant, xp_restante_pour_niveau_suivant).
        """
        lvl = 1
        for i, req in enumerate(XP_THRESHOLDS[1:], start=2):
            if xp < req:
                break
            lvl = i
        # Si on est au max de la table, pas de niveau suivant
        if lvl < len(XP_THRESHOLDS):
            to_next = XP_THRESHOLDS[lvl] - xp
        else:
            to_next = 0
        return lvl, to_next
