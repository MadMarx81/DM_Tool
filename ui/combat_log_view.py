import os
import tkinter as tk
from tkinter import ttk
from datetime import datetime

LOG_FILE = os.path.join("data", "combat_log.txt")

class CombatLogView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(padding=10)

        ttk.Label(self, text="📖 Journal des combats", font=("Helvetica", 14, "bold")).pack(pady=5)

        self.text = tk.Text(self, wrap="word", state="disabled", bg="#1e1e1e", fg="#e0e0e0", font=("Consolas", 10))
        self.text.pack(fill="both", expand=True)

        self.refresh_log()
        self.after(3000, self.auto_refresh)

    def add_log(self, message):
        # Écrit dans le fichier log
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(message + "\n")

        self.refresh_log()  # Met à jour l'affichage immédiatement

    def refresh_log(self):
        self.text.config(state="normal")
        self.text.delete("1.0", tk.END)

        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in reversed(lines):  # Affiche du plus récent au plus ancien
                    self.text.insert("end", line.strip() + "\n")
        else:
            self.text.insert("end", "Aucun combat enregistré.\n")

        self.text.config(state="disabled")

    def auto_refresh(self):
        self.refresh_log()
        self.after(3000, self.auto_refresh)  # rafraîchit toutes les 3 sec
