import tkinter as tk
import random

class InitiativeTracker(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.entities = []  # liste de dicts {name, hp, ac, status, init}
        self.build_ui()

    def build_ui(self):
        # --- Section d'ajout d'entité ---
        frm_add = tk.Frame(self)
        frm_add.pack(fill="x", pady=10)

        tk.Label(frm_add, text="Nom").grid(row=0, column=0)
        tk.Label(frm_add, text="PV").grid(row=0, column=1)
        tk.Label(frm_add, text="CA").grid(row=0, column=2)
        tk.Label(frm_add, text="État").grid(row=0, column=3)
        tk.Label(frm_add, text="Init").grid(row=0, column=4)

        self.e_name   = tk.Entry(frm_add, width=15); self.e_name.grid(row=1, column=0)
        self.e_hp     = tk.Entry(frm_add, width=5);  self.e_hp.grid(row=1, column=1)
        self.e_ac     = tk.Entry(frm_add, width=5);  self.e_ac.grid(row=1, column=2)
        self.e_status = tk.Entry(frm_add, width=10); self.e_status.grid(row=1, column=3)
        self.e_init   = tk.Entry(frm_add, width=5);  self.e_init.grid(row=1, column=4)

        btn_roll = tk.Button(frm_add, text="🎲 Roll Init", command=self.roll_init)
        btn_roll.grid(row=1, column=5, padx=5)
        btn_add  = tk.Button(frm_add, text="➕ Ajouter",   command=self.add_entity)
        btn_add.grid(row=1, column=6, padx=5)

        # --- Section d'affichage ---
        self.lst = tk.Listbox(self, font=("Consolas", 12))
        self.lst.pack(fill="both", expand=True, padx=10, pady=10)

    def roll_init(self):
        try:
            mod = int(self.e_init.get())
        except ValueError:
            mod = 0
        roll = random.randint(1, 20) + mod
        self.e_init.delete(0, tk.END)
        self.e_init.insert(0, str(roll))

    def add_entity(self):
        name = self.e_name.get().strip()
        try:
            hp = int(self.e_hp.get())
            ac = int(self.e_ac.get())
        except ValueError:
            return  # tu pourras ajouter un message d'erreur plus tard
        status = self.e_status.get().strip()
        try:
            init = int(self.e_init.get())
        except ValueError:
            init = 0

        self.entities.append({
            "name": name, "hp": hp, "ac": ac,
            "status": status, "init": init
        })
        self.refresh_list()

    def refresh_list(self):
        # trie décroissant par init
        self.entities.sort(key=lambda e: e["init"], reverse=True)
        self.lst.delete(0, tk.END)
        for e in self.entities:
            line = f'{e["init"]:>3} • {e["name"]:<12} HP:{e["hp"]:<3} CA:{e["ac"]:<2} [{e["status"]}]'
            self.lst.insert(tk.END, line)
