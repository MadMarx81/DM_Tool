import os
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from theme import setup_styles

class CombatLogView(ttk.Frame):
    """
    Journal des combats, écrit dans data/<system>/combat_log.txt
    """
    def __init__(self, parent, system=None, **kwargs):
        """
        :param system: GameSystem pour déterminer le dossier de log
        """
        setup_styles()
        super().__init__(parent, style="Custom.TFrame", padding=10, **kwargs)
        self.system = system
        base = system.name() if system else "dnd5e"
        self.log_file = os.path.join("data", base, "combat_log.txt")
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

        ttk.Label(
            self, text="📖 Journal des combats", style="Custom.Heading"
        ).pack(pady=5)

        self.text = tk.Text(
            self, wrap="word", state="disabled",
            bg="#1e1e1e", fg="#e0e0e0", font=("Consolas",10), relief="flat"
        )
        self.text.pack(fill="both", expand=True)

        self.refresh_log()
        self.after(3000, self.auto_refresh)

    def add_log(self, message):
        """Ajoute un message au journal et met à jour l'affichage"""
        ts = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        line = f"[{ts}] {message}"
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(line + "\n")
        self.refresh_log()

    def refresh_log(self):
        """Recharge et affiche le journal, ordre inverse (plus récent en haut)"""
        self.text.config(state="normal")
        self.text.delete("1.0", tk.END)
        if os.path.exists(self.log_file):
            with open(self.log_file, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
            for line in reversed(lines):
                self.text.insert("end", line + "\n")
        else:
            self.text.insert("end", "Aucun combat enregistré.\n")
        self.text.config(state="disabled")

    def auto_refresh(self):
        """Rafraîchit périodiquement"""
        self.refresh_log()
        self.after(3000, self.auto_refresh)
