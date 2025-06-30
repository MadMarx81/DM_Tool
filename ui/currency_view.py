import tkinter as tk
from tkinter import ttk

class CurrencyConverter(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.vars = {
            "pp": tk.IntVar(value=0),
            "po": tk.IntVar(value=0),
            "pa": tk.IntVar(value=0),
            "pc": tk.IntVar(value=0),
            "players": tk.IntVar(value=1),
        }

        # Labels + entrées
        row = 0
        for label in ["pp", "po", "pa", "pc"]:
            ttk.Label(self, text=f"{label.upper()} :").grid(row=row, column=0, sticky="e", padx=5, pady=2)
            ttk.Entry(self, textvariable=self.vars[label], width=10).grid(row=row, column=1, padx=5)
            row += 1

        ttk.Label(self, text="👥 Joueurs :").grid(row=row, column=0, sticky="e", padx=5, pady=2)
        ttk.Entry(self, textvariable=self.vars["players"], width=5).grid(row=row, column=1)
        row += 1

        ttk.Button(self, text="💰 Calculer", command=self.calculate).grid(row=row, columnspan=2, pady=10)
        row += 1

        self.result_label = ttk.Label(self, text="")
        self.result_label.grid(row=row, column=0, columnspan=2, pady=10)

    def calculate(self):
        try:
            pp = self.vars["pp"].get()
            po = self.vars["po"].get()
            pa = self.vars["pa"].get()
            pc = self.vars["pc"].get()
            players = max(1, self.vars["players"].get())

            # Conversion tout en pièces d'or
            total_po = pp * 10 + po + pa / 10 + pc / 100
            share = total_po / players

            self.result_label.config(
                text=f"💰 Total : {total_po:.2f} po\n👤 Par joueur : {share:.2f} po"
            )
        except Exception as e:
            self.result_label.config(text=f"Erreur : {e}")
