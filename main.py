#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
from ui.initiative_tracker import InitiativeTracker
from ui.bestiary_view import BestiaryView
from ui.notes_view import NotesView
from ui.spellbook_view import SpellbookView
from ui.calculators_view import CalculatorsView
from ui.party_view import PartyView
from ui.combat_log_view import CombatLogView
from ui.quest_journal_view import QuestJournalView
from ui.custom_grid_view import CustomGridViewPaned

class TabsView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True)

        # Onglet Initiative
        tracker = InitiativeTracker(notebook)
        notebook.add(tracker, text="🎲 Initiative")

        # Bestiaire
        bestiary = BestiaryView(notebook, tracker=tracker)
        notebook.add(bestiary, text="🐉 Bestiaire")

        # Notes
        notes = NotesView(notebook)
        notebook.add(notes, text="📓 Notes")

        # Sorts
        spellbook = SpellbookView(notebook)
        notebook.add(spellbook, text="📖 Sorts")

        # Calculs
        calculators = CalculatorsView(notebook, tracker=tracker)
        notebook.add(calculators, text="🧮 Calculs")

        # Journal de combat
        log_tab = CombatLogView(notebook)
        notebook.add(log_tab, text="📖 Journal")

        # Joueurs
        party = PartyView(notebook, tracker=tracker, xp_calculator=calculators, log_view=log_tab)
        notebook.add(party, text="👥 Joueurs")
        calculators.xp_calculator.party_view = party

        # Journal de quêtes
        quests_tab = QuestJournalView(notebook)
        notebook.add(quests_tab, text="🗺️ Quêtes")

class GridView(ttk.Frame):
    def __init__(self, parent, rows=2, cols=2):
        super().__init__(parent)
        # crénaux de grille
        for r in range(rows): self.rowconfigure(r, weight=1)
        for c in range(cols): self.columnconfigure(c, weight=1)

        # on place les mêmes vues dans chaque cellule
        # tu pourras les instancier à part si besoin
        widgets = [
            InitiativeTracker, BestiaryView, NotesView, SpellbookView,
            # etc. adapte la liste à rows*cols
        ]
        idx = 0
        for r in range(rows):
            for c in range(cols):
                if idx < len(widgets):
                    frame = widgets[idx](self)
                    frame.grid(row=r, column=c, sticky="nsew", padx=5, pady=5)
                idx += 1

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DM Tool")
        self.geometry("1200x800")

        self.views = {}

        self.available_views = {
            "Initiative": InitiativeTracker,
            "Bestiaire": BestiaryView,
            "Notes": NotesView,
            "Sorts": SpellbookView,
            "Calculs": CalculatorsView,
            "Joueurs": PartyView,
            "Combat log": CombatLogView,
            "Quêtes": QuestJournalView,
        }

        # Tabs mode
        self.views['tabs'] = TabsView(self)

        # Custom Grid Mode
        from ui.custom_grid_view import CustomGridViewPaned
        self.views['custom'] = CustomGridViewPaned(self, rows=2, cols=2, available_views=self.available_views)


        for view in self.views.values():
            view.grid(row=0, column=0, sticky="nsew")

        self.show_view('tabs')

        # Menu
        menubar = tk.Menu(self)
        view_menu = tk.Menu(menubar, tearoff=False)
        view_menu.add_command(label="Mode Onglets", command=lambda: self.show_view('tabs'))
        view_menu.add_command(label="Vue 2x2", command=lambda: self._switch_custom_grid(2, 2))
        view_menu.add_command(label="Vue 3x2", command=lambda: self._switch_custom_grid(2, 3))
        menubar.add_cascade(label="Affichage", menu=view_menu)
        self.config(menu=menubar)

    def _switch_custom_grid(self, rows, cols):
        self.views['custom'].destroy()
        self.views['custom'] = CustomGridViewPaned(self, rows=rows, cols=cols, available_views=self.available_views)
        self.views['custom'].grid(row=0, column=0, sticky="nsew")
        self.show_view('custom')

    def show_view(self, name):
        self.views[name].tkraise()


if __name__ == '__main__':
    app = MainApp()
    app.mainloop()
