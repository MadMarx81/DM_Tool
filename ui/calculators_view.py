import tkinter as tk
from tkinter import ttk
from ui.currency_converter import CurrencyConverter
from ui.travel_calculator import TravelCalculator
from ui.xp_calculator import XPCombatCalculator

class CalculatorsView(ttk.Frame):
    def __init__(self, parent, tracker=None, system=None, party_view=None, characters_dir="data/characters"):
        super().__init__(parent)
        self.tracker = tracker
        self.system = system
        self.party_view = party_view
        self.characters_dir = characters_dir

        # Notebook interne pour les calculateurs
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True, padx=10, pady=10)

        # Onglet Convertisseur de devises
        frame_currency = ttk.Frame(self.tabs)
        conv = CurrencyConverter(frame_currency)
        conv.pack(fill="both", expand=True)
        self.tabs.add(frame_currency, text="💰 Devises")

        # Onglet Calcul de voyage
        frame_travel = ttk.Frame(self.tabs)
        travel = TravelCalculator(frame_travel)
        travel.pack(fill="both", expand=True)
        self.tabs.add(frame_travel, text="🚶 Voyage")

        # Onglet XP Combat
        frame_xp = ttk.Frame(self.tabs)
        self.xp_calculator = XPCombatCalculator(
            frame_xp,
            tracker=self.tracker,
            characters_dir=self.characters_dir,
            party_view=self.party_view,
            system=self.system
        )
        self.xp_calculator.pack(fill="both", expand=True)
        self.tabs.add(frame_xp, text="🏆 XP Combat")
