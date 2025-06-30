import tkinter as tk
from tkinter import ttk, messagebox

class XPCombatCalculator(ttk.Frame):
    def __init__(self, parent, tracker=None):
        super().__init__(parent)
        self.tracker = tracker  # référence à l'initiative tracker
        self.player_count = 1   # nombre de joueurs par défaut

        # Table officielle d'XP par CR (à compléter selon ta référence)
        self.xp_per_cr = {
            '0': 10, '1/8': 25, '1/4': 50, '1/2': 100,
            '1': 200, '2': 450, '3': 700, '4': 1100,
            '5': 1800, '6': 2300, '7': 2900, '8': 3900,
            '9': 5000, '10': 5900
            # … jusqu'au CR maximal que tu utilises
        }

        # Bouton de calcul
        ttk.Button(self, text="🔄 Calculer XP", command=self.calculate_xp).pack(pady=10)
        # Label pour afficher le résultat
        self.result = ttk.Label(self, text="", justify="center", font=("Consolas", 11))
        self.result.pack(pady=10)

    def set_player_count(self, count):
        """Permet de définir le nombre de joueurs imported depuis PartyView."""
        self.player_count = max(1, int(count))

    def calculate_xp(self):
        if not self.tracker:
            messagebox.showwarning("Pas de tracker", "Aucun tracker d'initiative fourni.")
            return

        total_xp = 0
        # Parcours des entités : on compte uniquement les monstres morts
        for ent in getattr(self.tracker, 'entities', []):
            if ent.get('is_monster', False) and ent.get('hp', 1) <= 0:
                cr = str(ent.get('challenge_rating', '0'))
                xp = self.xp_per_cr.get(cr, 0)
                total_xp += xp

        per_player = total_xp / self.player_count

        # Affichage du résultat
        self.result.config(
            text=(f"XP total du combat : {total_xp}\n"
                  f"Joueurs : {self.player_count} → XP/joueur : {per_player:.2f}")
        )
