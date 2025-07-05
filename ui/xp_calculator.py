import os
import json
import tkinter as tk
from tkinter import ttk, messagebox

class XPCombatCalculator(ttk.Frame):
    """
    Calculateur d'XP de combat, basé sur un système de jeu générique.
    """
    def __init__(
        self, parent,
        tracker=None,
        characters_dir=None,
        party_view=None,
        system=None,
        **kwargs
    ):
        """
        :param tracker: InitiativeTracker
        :param characters_dir: chemin dossier persos (sera construit via system.name())
        :param party_view: PartyView pour rafraîchir et logger
        :param system: GameSystem définissant xp_for_cr(), compute_level(), name(), etc.
        """
        super().__init__(parent, style="Custom.TFrame", **kwargs)
        self.tracker = tracker
        self.party_view = party_view
        self.system = system

        # Dossier personnages
        base = system.name() if system else "dnd5e"
        self.characters_dir = characters_dir or os.path.join("data", base, "characters")

        # UI
        self.btn = ttk.Button(self, text="🔄 Calculer XP", command=self.calculate_xp, style="Custom.TButton")
        self.btn.pack(pady=10)
        self.result = ttk.Label(self, text="", justify="center", style="Custom.TLabel")
        self.result.pack(pady=10)

    def calculate_xp(self):
        if not self.tracker:
            messagebox.showwarning("Pas de tracker", "Aucun tracker fourni.")
            return
        if not self.system:
            messagebox.showwarning("Pas de système", "Aucun système de jeu fourni.")
            return

        total_xp = 0
        # Somme des XP via la logique du système
        for ent in getattr(self.tracker, 'entities', []):
            if ent.get('is_monster') and ent.get('hp', 1) <= 0:
                cr = str(ent.get('challenge_rating', '0'))
                total_xp += self.system.xp_for_cr(cr)

        # Répartir
        players = [e for e in self.tracker.entities if not e.get('is_monster')]
        count = len(players) or 1
        per_player = total_xp / count

        # Mise à jour JSON des persos
        for ent in players:
            name = ent['name']
            path = os.path.join(self.characters_dir, f"{name}.json")
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                old_xp = data.get('xp', 0)
                new_xp = old_xp + per_player
                data['xp'] = int(new_xp)
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

        # Log
        monsters = [ent for ent in self.tracker.entities if ent.get('is_monster')]
        if self.party_view and hasattr(self.party_view, 'log_combat'):
            self.party_view.log_combat(total_xp, monsters, players)

        # Affichage
        self.result.config(text=f"XP total: {total_xp}\nJoueurs: {count} → {per_player:.2f} chacun")

        # Rafraîchir partie view
        if self.party_view and hasattr(self.party_view, 'show_character_summary'):
            self.party_view.show_character_summary()
