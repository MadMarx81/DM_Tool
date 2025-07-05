# ui/travel_calculator.py

import tkinter as tk
from tkinter import ttk

class TravelCalculator(ttk.Frame):
    def __init__(self, parent, system, **kwargs):
        """
        :param system: instance de GameSystem (e.g. DnD5eSystem, StarfinderSystem)
        """
        super().__init__(parent, **kwargs)
        self.system = system

        # Variables
        self.distance_var = tk.DoubleVar(value=0.0)
        self.speed_var    = tk.StringVar(value="normal")

        # Récupère les modes de déplacement et leurs vitesses (km/jour)
        # attend que GameSystem implémente `daily_speeds() -> dict[str, float]`
        self.speed_values = self.system.daily_speeds()

        # UI
        ttk.Label(self, text=f"📏 Distance ({self.system.distance_units()}):")\
           .grid(row=0, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(self, textvariable=self.distance_var, width=10)\
           .grid(row=0, column=1)

        ttk.Label(self, text="🚶‍♂️ Mode de déplacement :")\
           .grid(row=1, column=0, sticky="e", padx=5, pady=5)
        speed_menu = ttk.OptionMenu(
            self, self.speed_var, self.speed_var.get(), *self.speed_values.keys()
        )
        speed_menu.grid(row=1, column=1)

        ttk.Button(self, text="📍 Calculer", command=self.calculate)\
           .grid(row=2, columnspan=2, pady=10)

        self.result_label = ttk.Label(self, text="")
        self.result_label.grid(row=3, column=0, columnspan=2, pady=10)

    def calculate(self):
        try:
            # On suppose que la distance entrée est en unités système
            dist = self.distance_var.get()
            mode = self.speed_var.get()
            speed = self.speed_values.get(mode, 0)

            # Temps en jours
            days = dist / speed if speed else float('inf')
            full_days = int(days)
            hours = int((days - full_days) * 24)

            self.result_label.config(
                text=f"⏳ Temps estimé : {full_days} jours, {hours} heures"
            )
        except Exception as e:
            self.result_label.config(text=f"Erreur : {e}")
