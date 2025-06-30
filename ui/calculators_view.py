import tkinter as tk
from tkinter import ttk
from ui.currency_converter import CurrencyConverter
from ui.travel_calculator import TravelCalculator
from ui.xp_calculator import XPCombatCalculator

class CalculatorsView(tk.Frame):
    def __init__(self, parent, tracker):
        super().__init__(parent, bg="#e6e2d3")
        self.tracker = tracker

        tabs = ttk.Notebook(self)
        tabs.pack(fill="both", expand=True, padx=5, pady=5)

        # Onglet Convertisseur de devises
        frame_currency = tk.Frame(tabs, bg="#e6e2d3")
        conv = CurrencyConverter(frame_currency)
        conv.pack(fill="both", expand=True)
        tabs.add(frame_currency, text="💰 Devises")

        # Onglet Calcul de voyage
        frame_travel = tk.Frame(tabs, bg="#e6e2d3")
        travel = TravelCalculator(frame_travel)
        travel.pack(fill="both", expand=True)
        tabs.add(frame_travel, text="🚶 Voyage")

        # Onglet XP Combat
        frame_xp = tk.Frame(tabs, bg="#e6e2d3")
        xp = XPCombatCalculator(frame_xp, tracker=self.tracker)
        xp.pack(fill="both", expand=True)
        tabs.add(frame_xp, text="🏆 XP Combat")
