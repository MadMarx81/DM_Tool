import tkinter as tk
from tkinter import ttk
from ui.initiative_tracker import InitiativeTracker
from ui.bestiary_view import BestiaryView
from ui.notes_view import NotesView
from ui.spellbook_view import SpellbookView
from ui.calculators_view import CalculatorsView
from ui.party_view import PartyView


def main():
    root = tk.Tk()
    root.title("DM Tool – Tableau de bord DnD")
    root.geometry("800x600")

    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)

    # Onglet Initiative
    tracker = InitiativeTracker(notebook)
    notebook.add(tracker, text="🎲 Initiative")

    # Onglet Bestiaire, on lui passe le tracker pour ajout
    bestiary = BestiaryView(notebook, tracker=tracker)
    notebook.add(bestiary, text="🐉 Bestiaire")

    # Onglet Notes
    notes = NotesView(notebook)
    notebook.add(notes, text="📓 Notes")

    # Onglet Sorts
    spellbook = SpellbookView(notebook)
    notebook.add(spellbook, text="📖 Sorts")

    # Onglet Calculs — **UNIQUEMENT** avec le tracker
    calculators = CalculatorsView(notebook, tracker=tracker)
    notebook.add(calculators, text="🧮 Calculs")

    party = PartyView(notebook, tracker=tracker, xp_calculator=calculators)
    notebook.add(party, text="👥 Joueurs")

    root.mainloop()

if __name__ == '__main__':
    main()
