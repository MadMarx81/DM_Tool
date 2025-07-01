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

def main():
    root = tk.Tk()
    root.title("DM Tool – Tableau de bord DnD")
    root.geometry("800x600")

    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)

    # Onglet Initiative
    tracker = InitiativeTracker(notebook)
    notebook.add(tracker, text="🎲 Initiative")

    # Onglet Bestiaire
    bestiary = BestiaryView(notebook, tracker=tracker)
    notebook.add(bestiary, text="🐉 Bestiaire")

    # Onglet Notes
    notes = NotesView(notebook)
    notebook.add(notes, text="📓 Notes")

    # Onglet Sorts
    spellbook = SpellbookView(notebook)
    notebook.add(spellbook, text="📖 Sorts")

    # Onglet Calculs (créé avant PartyView mais temporairement sans party_view)
    calculators = CalculatorsView(notebook, tracker=tracker)
    notebook.add(calculators, text="🧮 Calculs")

    # Onglet Journal
    log_tab = CombatLogView(notebook)
    notebook.add(log_tab, text="📖 Journal")

    # Onglet Joueurs (on transmet calculators pour qu’il soit mis à jour avec le party)
    party = PartyView(notebook, tracker=tracker, xp_calculator=calculators, log_view=log_tab)
    notebook.add(party, text="👥 Joueurs")

    # ✅ Mise à jour du XPCalculator avec PartyView (pour le log combat !)
    calculators.xp_calculator.party_view = party

    root.mainloop()

if __name__ == '__main__':
    main()
