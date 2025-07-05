# systems/dnd5e.py
import random
from .base import GameSystem

# Copier ici tes tables depuis XPCombatCalculator & PartyView
XP_PER_CR = {
    '0': 10, '1/8': 25, '1/4': 50, '1/2': 100,
    '1': 200, '2': 450, '3': 700, '4': 1100,
    '5': 1800, '6': 2300, '7': 2900, '8': 3900,
    '9': 5000, '10': 5900
}
XP_THRESHOLDS = [0,300,900,2700,6500,14000,23000,34000,48000,64000,
                 85000,100000,120000,140000,165000,195000,225000,265000,305000,355000]

class DnD5eSystem(GameSystem):
    def name(self) -> str:
        return "dnd5e"

    def initiative(self, actor: dict) -> int:
        # Jet standard d20 + mod init
        roll = random.randint(1,20)
        return roll + actor.get('init_mod', 0)

    def xp_for_cr(self, cr: str) -> int:
        return XP_PER_CR.get(str(cr), 0)

    def compute_level(self, xp: int) -> tuple[int,int]:
        lvl = 1
        for i, req in enumerate(XP_THRESHOLDS, start=1):
            if xp < req:
                break
            lvl = i
        next_req = XP_THRESHOLDS[lvl] if lvl < len(XP_THRESHOLDS) else XP_THRESHOLDS[-1]
        return lvl, next_req - xp
