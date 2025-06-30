import tkinter as tk
from tkinter import ttk
from ui.currency_converter import CurrencyConverter
from ui.travel_calculator import TravelCalculator
from ui.xp_calculator import XPCombatCalculator

class CalculatorsView(ttk.Frame):
    def __init__(self, parent, tracker):
        super().__init__(parent)
        self.tracker = tracker  # On garde la référence du tracker ici

        tabs = ttk.Notebook(self)
        tabs.pack(fill="both", expand=True)

        # Onglet Convertisseur de devises
        tabs.add(CurrencyConverter(tabs), text="💰 Devises")

        # Onglet Calcul de voyage
        tabs.add(TravelCalculator(tabs), text="🚶 Voyage")

        # Onglet XP Combat, on lui passe le tracker pour lire entities
        tabs.add(XPCombatCalculator(tabs, tracker=self.tracker), text="🏆 XP Combat")
