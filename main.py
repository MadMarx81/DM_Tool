#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
from systems.dnd5e import DnD5eSystem
# Importer d'autres systèmes si disponibles
from systems.starfinder import StarfinderSystem
# from systems.shadowrun import ShadowrunSystem

from ui.initiative_tracker import InitiativeTracker
from ui.bestiary_view import BestiaryView
from ui.notes_view import NotesView
from ui.spellbook_view import SpellbookView
from ui.calculators_view import CalculatorsView
from ui.party_view import PartyView
from ui.combat_log_view import CombatLogView
from ui.quest_journal_view import QuestJournalView
from ui.custom_grid_view import CustomGridViewPaned

class MainApp(tk.Tk):
    def __init__(self, systems):
        super().__init__()
        self.title("DM Tool – Tableau de bord")
        self.geometry("1920x1080")

        # Stocke les systèmes disponibles
        self.systems = systems  # dict: {"Nom affiché": instance_system}
        # Variable pour le choix courant
        self.current_system_var = tk.StringVar(value=list(systems.keys())[0])

        # Sélecteur de système en haut
        selector_frame = ttk.Frame(self, padding=5)
        selector_frame.grid(row=0, column=0, sticky="ew")
        selector_frame.columnconfigure(1, weight=1)
        ttk.Label(selector_frame, text="Système :", style="Custom.TLabel").grid(row=0, column=0, padx=(0,5))
        self.system_selector = ttk.Combobox(
            selector_frame,
            textvariable=self.current_system_var,
            values=list(self.systems.keys()),
            state="readonly",
            style="Custom.TEntry"
        )
        self.system_selector.grid(row=0, column=1, sticky="ew")
        self.system_selector.bind("<<ComboboxSelected>>", self._on_system_change)

        # Conteneur pour les onglets
        self.container = ttk.Frame(self)
        self.container.grid(row=1, column=0, sticky="nsew")
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # Construire les onglets pour le système initial
        initial_system = self.systems[self.current_system_var.get()]
        self._build_tabs(self.container, initial_system)

    def _build_tabs(self, parent, system):
        # Détruit l'ancien notebook s'il existait
        if hasattr(self, 'notebook'):
            self.notebook.destroy()

        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill='both', expand=True)

        # Onglets
        tracker = InitiativeTracker(self.notebook, system=system)
        self.notebook.add(tracker, text="🎲 Initiative")

        bestiary = BestiaryView(self.notebook, tracker=tracker, system=system)
        self.notebook.add(bestiary, text="🐉 Bestiaire")

        notes = NotesView(self.notebook)
        self.notebook.add(notes, text="📓 Notes")

        spellbook = SpellbookView(self.notebook, system=system)
        self.notebook.add(spellbook, text="📖 Sorts")

        calculators = CalculatorsView(
            self.notebook,
            tracker=tracker,
            system=system,
            party_view=None
        )
        self.notebook.add(calculators, text="🧮 Calculs")

        combat_log = CombatLogView(self.notebook)
        self.notebook.add(combat_log, text="📖 Journal")

        party = PartyView(
            self.notebook,
            tracker=tracker,
            xp_calculator=calculators.xp_calculator,
            log_view=combat_log,
            system=system
        )
        self.notebook.add(party, text="👥 Joueurs")
        # Lie la vue Party à l'XP Calculator
        calculators.xp_calculator.party_view = party

        quests = QuestJournalView(self.notebook)
        self.notebook.add(quests, text="🗺️ Quêtes")

    def _on_system_change(self, event=None):
        name = self.current_system_var.get()
        system = self.systems[name]
        self._build_tabs(self.container, system)

if __name__ == '__main__':
    # Instancier les systèmes de jeu disponibles
    systems = {
        "D&D 5e": DnD5eSystem(),
        "Starfinder": StarfinderSystem(),
        # "Shadowrun": ShadowrunSystem(),
    }
    app = MainApp(systems)
    app.mainloop()
