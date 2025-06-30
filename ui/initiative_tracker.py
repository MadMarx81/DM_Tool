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
        frm_list = tk.Frame(self)
        frm_list.pack(fill="both", expand=True, padx=10, pady=10)

        self.lst = tk.Listbox(frm_list, font=("Consolas", 12))
        self.lst.pack(side="left", fill="both", expand=True)

        # Barre de défilement
        scrollbar = tk.Scrollbar(frm_list, orient="vertical", command=self.lst.yview)
        scrollbar.pack(side="right", fill="y")
        self.lst.config(yscrollcommand=scrollbar.set)

        # Bouton de suppression
        btn_delete = tk.Button(self, text="🗑️ Supprimer sélection", command=self.delete_entity)
        btn_delete.pack(pady=5)

    def roll_init(self):
        # Effacer l'ancien roll avant d'insérer le nouveau
        self.e_init.delete(0, tk.END)
        try:
            mod = int(self.e_init.get())
        except ValueError:
            mod = 0
        roll = random.randint(1, 20) + mod
        self.e_init.insert(0, str(roll))

    def add_entity(self):
        name = self.e_name.get().strip()
        try:
            hp = int(self.e_hp.get())
            ac = int(self.e_ac.get())
        except ValueError:
            return  # plus tard : afficher un message d'erreur
        status = self.e_status.get().strip()
        try:
            init = int(self.e_init.get())
        except ValueError:
            init = 0

        self.entities.append({
            "name": name,
            "hp": hp,
            "ac": ac,
            "status": status,
            "init": init
        })
        self.clear_entries()
        self.refresh_list()

    def delete_entity(self):
        # Supprime l'entité sélectionnée dans la liste
        sel = self.lst.curselection()
        if sel:
            idx = sel[0]
            del self.entities[idx]
            self.refresh_list()

    def clear_entries(self):
        # Efface tous les champs d'entrée après ajout
        self.e_name.delete(0, tk.END)
        self.e_hp.delete(0, tk.END)
        self.e_ac.delete(0, tk.END)
        self.e_status.delete(0, tk.END)
        self.e_init.delete(0, tk.END)

    def refresh_list(self):
        # Trie décroissant par initiative
        self.entities.sort(key=lambda e: e["init"], reverse=True)
        self.lst.delete(0, tk.END)
        for e in self.entities:
            line = f'{e["init"]:>3} • {e["name"]:<12} HP:{e["hp"]:<3} CA:{e["ac"]:<2} [{e["status"]}]'
            self.lst.insert(tk.END, line)
