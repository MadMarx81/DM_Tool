import tkinter as tk
from tkinter import ttk

class TravelCalculator(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.distance_var = tk.DoubleVar(value=0.0)
        self.speed_var = tk.StringVar(value="normal")

        speeds = {
            "normal": 38,
            "rapide": 48,
            "lente": 30,
            "monture": 64,
            "difficile": 20,
        }

        self.speed_values = speeds

        # Entrées
        ttk.Label(self, text="📏 Distance (km) :").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        ttk.Entry(self, textvariable=self.distance_var, width=10).grid(row=0, column=1)

        ttk.Label(self, text="🚶‍♂️ Mode de déplacement :").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        speed_menu = ttk.OptionMenu(self, self.speed_var, "normal", *speeds.keys())
        speed_menu.grid(row=1, column=1)

        ttk.Button(self, text="📍 Calculer", command=self.calculate).grid(row=2, columnspan=2, pady=10)

        self.result_label = ttk.Label(self, text="")
        self.result_label.grid(row=3, column=0, columnspan=2, pady=10)

    def calculate(self):
        try:
            distance = self.distance_var.get()
            speed_key = self.speed_var.get()
            km_per_day = self.speed_values.get(speed_key, 38)

            days = distance / km_per_day
            full_days = int(days)
            hours = round((days - full_days) * 24)

            self.result_label.config(
                text=f"⏳ Temps estimé : {full_days} jours et {hours} heures"
            )
        except Exception as e:
            self.result_label.config(text=f"Erreur : {e}")
