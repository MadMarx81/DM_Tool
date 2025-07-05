# systems/base.py
from abc import ABC, abstractmethod

class GameSystem(ABC):
    """Interface abstraite pour un moteur de JDR (initiative, XP, niveaux, etc.)."""

    @abstractmethod
    def name(self) -> str:
        """Identifiant unique du système (ex. 'dnd5e')."""
        pass

    @abstractmethod
    def initiative(self, actor: dict) -> int:
        """Calcule le jet d’initiative d’un acteur."""
        pass

    @abstractmethod
    def xp_for_cr(self, cr: str) -> int:
        """Retourne l’XP attribuée pour un monstre de CR donné."""
        pass

    @abstractmethod
    def compute_level(self, xp: int) -> tuple[int,int]:
        """
        Retourne (niveau, xp_requise_pour_niveau_suivant)
        selon les seuils du système.
        """
        pass
