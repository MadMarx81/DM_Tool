import os
import json
import tkinter as tk
from tkinter import ttk, messagebox

class XPCombatCalculator(ttk.Frame):
    def __init__(self, parent, tracker=None, characters_dir="data/characters", party_view=None):
        super().__init__(parent)
        self.tracker = tracker
        self.characters_dir = characters_dir
        self.party_view = party_view  # pour rafraîchir l'affichage du PartyView et logger les combats

        # Table des XP par CR
        self.xp_per_cr = {
            '0': 10, '1/8': 25, '1/4': 50, '1/2': 100,
            '1': 200, '2': 450, '3': 700, '4': 1100,
            '5': 1800, '6': 2300, '7': 2900, '8': 3900,
            '9': 5000, '10': 5900
        }

        # Bouton de calcul
        self.btn = ttk.Button(self, text="🔄 Calculer XP", command=self.calculate_xp)
        self.btn.pack(pady=10)

        # Label pour afficher le résultat
        self.result = ttk.Label(self, text="", justify="center", font=("Consolas", 11))
        self.result.pack(pady=10)

    def calculate_xp(self):
        if not self.tracker:
            messagebox.showwarning("Pas de tracker", "Aucun tracker fourni.")
            return

        total_xp = 0

        # Somme des XP des monstres morts
        for ent in getattr(self.tracker, 'entities', []):
            if ent.get('is_monster') and ent.get('hp', 1) <= 0:
                cr = str(ent.get('challenge_rating', '0'))
                total_xp += self.xp_per_cr.get(cr, 0)

        # Répartition entre joueurs
        players = [e for e in self.tracker.entities if not e.get('is_monster')]
        count = len(players) or 1
        per_player = total_xp / count

        # Mise à jour des fichiers JSON des personnages
        for ent in players:
            name = ent['name']
            path = os.path.join(self.characters_dir, f"{name}.json")
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                data['xp'] = data.get('xp', 0) + per_player
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

        # Logger le combat via PartyView s’il existe
        monsters = [ent for ent in self.tracker.entities if ent.get('is_monster')]
        if self.party_view and hasattr(self.party_view, 'log_combat'):
            self.party_view.log_combat(total_xp, monsters, players)

        # Affichage dans le label
        self.result.config(text=f"XP total: {total_xp}\nJoueurs: {count} → {per_player:.2f} chacun")

        # Rafraîchissement de la vue des personnages
        if self.party_view and hasattr(self.party_view, 'show_character_summary'):
            self.party_view.show_character_summary()
