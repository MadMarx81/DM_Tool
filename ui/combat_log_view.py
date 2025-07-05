import os
import tkinter as tk
from tkinter import ttk

class CombatLogView(ttk.Frame):
    def __init__(self, parent, system=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.system = None
        self.log_path = None

        self.text = tk.Text(self, bg="#f9f7f0", fg="#5c4d3d", font=("Consolas", 11), state='disabled')
        self.text.pack(fill='both', expand=True)

        if system is not None:
            self.set_system(system)

    def set_system(self, system):
        # Met à jour le système et recharge le log
        self.system = system
        system_name = system.name() if callable(getattr(system, 'name', None)) else str(system)
        base_dir = os.path.join("data", system_name)
        os.makedirs(base_dir, exist_ok=True)
        self.log_path = os.path.join(base_dir, "combat_log.txt")
        self.reload_log()

    def reload_log(self):
        self.text.config(state='normal')
        self.text.delete('1.0', 'end')
        if self.log_path and os.path.exists(self.log_path):
            with open(self.log_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.text.insert('end', content)
        self.text.config(state='disabled')

    def append_log(self, message):
        # Exemple fonction pour ajouter un message et sauvegarder dans le fichier
        if not self.log_path:
            return
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(message + "\n")
        self.text.config(state='normal')
        self.text.insert('end', message + "\n")
        self.text.config(state='disabled')
        self.text.see('end')
