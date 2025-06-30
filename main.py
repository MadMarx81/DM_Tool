import tkinter as tk
from tkinter import ttk
from ui.initiative_tracker import InitiativeTracker
from ui.bestiary_view import BestiaryView

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

    # Onglet sorts
    from ui.spellbook_view import SpellbookView

    spellbook = SpellbookView(notebook)
    notebook.add(spellbook, text="📖 Sorts")

    root.mainloop()


if __name__ == '__main__':
    main()
