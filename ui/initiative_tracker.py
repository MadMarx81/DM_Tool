import tkinter as tk
import random
from tkinter import simpledialog

class InitiativeTracker(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.entities = []
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

        tk.Button(frm_add, text="🎲 Roll Init", command=self.roll_init).grid(row=1, column=5, padx=5)
        tk.Button(frm_add, text="➕ Ajouter", command=self.add_entity).grid(row=1, column=6, padx=5)

        # --- Section d'affichage ---
        frm_list = tk.Frame(self)
        frm_list.pack(fill="both", expand=True, padx=10, pady=10)

        self.lst = tk.Listbox(frm_list, font=("Consolas", 12))
        self.lst.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(frm_list, orient="vertical", command=self.lst.yview)
        scrollbar.pack(side="right", fill="y")
        self.lst.config(yscrollcommand=scrollbar.set)

        # --- Section de contrôle des sélections ---
        frm_ctrl = tk.Frame(self)
        frm_ctrl.pack(fill="x", pady=5)
        tk.Button(frm_ctrl, text="🗑️ Supprimer sélection", command=self.delete_entity).pack(side="left", padx=5)
        tk.Button(frm_ctrl, text="🎲 Roll Init sélection", command=self.roll_selected).pack(side="left", padx=5)
        tk.Button(frm_ctrl, text="✏️ Modifier Init", command=self.edit_selected_init).pack(side="left", padx=5)

    def roll_init(self):
        # Effacer l'ancien roll avant d'insérer le nouveau
        self.e_init.delete(0, tk.END)
        try:
            mod = int(self.e_init.get())
        except ValueError:
            mod = 0
        roll = random.randint(1, 20) + mod
        self.e_init.insert(0, str(roll))

    def _read_entry(self):
        # Lecture des champs d'entrée, retourne dict ou None
        name = self.e_name.get().strip()
        try:
            hp = int(self.e_hp.get())
            ac = int(self.e_ac.get())
        except ValueError:
            return None
        status = self.e_status.get().strip()
        try:
            init = int(self.e_init.get())
        except ValueError:
            init = 0
        return {"name": name, "hp": hp, "ac": ac, "status": status, "init": init}

    def add_entity(self):
        entity = self._read_entry()
        if not entity:
            return
        self.entities.append(entity)
        self.clear_entries()
        self.refresh_list()

    def add_entity_obj(self, entity):
        # Ajout via code externe (BestiaryView)
        self.entities.append(entity)
        self.refresh_list()

    def delete_entity(self):
        sel = self.lst.curselection()
        if sel:
            del self.entities[sel[0]]
            self.refresh_list()

    def roll_selected(self):
        sel = self.lst.curselection()
        if not sel:
            return
        idx = sel[0]
        # Supposer mod est 0 ou stocké ailleurs, on reroll sans modif
        new_init = random.randint(1, 20)
        self.entities[idx]["init"] = new_init
        self.refresh_list()

    def edit_selected_init(self):
        sel = self.lst.curselection()
        if not sel:
            return
        idx = sel[0]
        current = self.entities[idx].get("init", 0)
        # Demande à l'utilisateur la nouvelle valeur
        new_val = simpledialog.askinteger("Modifier Initiative", "Nouvelle valeur d'initiative:", initialvalue=current)
        if new_val is not None:
            self.entities[idx]["init"] = new_val
            self.refresh_list()

    def clear_entries(self):
        for widget in (self.e_name, self.e_hp, self.e_ac, self.e_status, self.e_init):
            widget.delete(0, tk.END)

    def refresh_list(self):
        # Trie décroissant par initiative
        self.entities.sort(key=lambda e: e.get("init", 0), reverse=True)
        self.lst.delete(0, tk.END)
        for e in self.entities:
            line = f'{e.get("init",0):>3} • {e.get("name"," "): <12} HP:{e.get("hp"," "):<3} CA:{e.get("ac"," "):<2} [{e.get("status"," ")}]'
            self.lst.insert(tk.END, line)
