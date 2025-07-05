# systems/base.py
from abc import ABC, abstractmethod

class GameSystem(ABC):
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def initiative(self, actor: dict) -> int:
        ...

    @abstractmethod
    def xp_for_cr(self, cr: str) -> int:
        ...

    @abstractmethod
    def compute_level(self, xp: int) -> tuple[int,int]:
        ...

    # ← Ajoutez ces méthodes génériques pour la partie voyage
    @abstractmethod
    def distance_units(self) -> str:
        """
        Renvoie l’unité de distance utilisée par le système (ex: 'km', 'mi', 'ft').
        """
        pass

    @abstractmethod
    def daily_speeds(self) -> dict[str, float]:
        """
        Retourne un dict {mode: vitesse_en_unités_par_jour}.
        Exemple D&D 5e : {'normal': 24, 'rapide': 30, 'lente': 18}
        """
        pass
