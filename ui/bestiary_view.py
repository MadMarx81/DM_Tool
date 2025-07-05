import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import json
import os

class BestiaryView(ttk.Frame):
    """
    Affiche un bestiaire de monstres, dépendant du système de jeu passé.
    """
    CUSTOM_FILE = "custom_monsters.json"

    def __init__(self, master, tracker=None, system=None, **kwargs):
        """
        :param system: instance de GameSystem définissant name() et règles
        """
        super().__init__(master, style="Custom.TFrame", **kwargs)
        self.tracker = tracker
        self.system = system

        # Dossier de données des monstres pour le système
        base = system.name() if system else "dnd5e"
        self.data_dir = os.path.join("data", base, "monsters")
        os.makedirs(self.data_dir, exist_ok=True)
        self.custom_path = os.path.join(self.data_dir, self.CUSTOM_FILE)

        # Chargement et UI
        self.monsters = self.load_monsters()
        self.filtered_names = sorted(self.monsters.keys())
        self.build_ui()

    def load_monsters(self):
        monsters = {}
        # Charge tous les JSON (sauf custom)
        for filename in os.listdir(self.data_dir):
            if not filename.endswith('.json') or filename == self.CUSTOM_FILE:
                continue
            path = os.path.join(self.data_dir, filename)
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # Format listes ou objets
            if isinstance(data, dict) and 'monster' in data and isinstance(data['monster'], list):
                for entry in data['monster']:
                    name = entry.get('name')
                    if name:
                        monsters[name] = entry
            elif isinstance(data, dict) and 'name' in data:
                monsters[data['name']] = data

        # Charge le fichier custom si présent
        if os.path.exists(self.custom_path):
            with open(self.custom_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for entry in data.get('monster', []):
                name = entry.get('name')
                if name:
                    monsters[name] = entry
        return monsters

    def build_ui(self):
        frm_search = ttk.Frame(self, style="Custom.TFrame")
        frm_search.pack(fill='x', pady=5)
        ttk.Label(frm_search, text="Chercher:", style="Custom.TLabel").pack(side='left', padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace_add('write', self.on_search)
        ttk.Entry(frm_search, textvariable=self.search_var, style="Custom.TEntry").pack(side='left', fill='x', expand=True)

        frm_list = ttk.Frame(self, style="Custom.TFrame")
        frm_list.pack(fill='x', padx=10, pady=5)
        self.lst_monsters = tk.Listbox(
            frm_list,
            height=6,
            font=("Consolas", 11),
            bg="white",
            fg="black",
            selectbackground="#cce6ff"
        )
        self.lst_monsters.pack(side='left', fill='x', expand=True)
        sb = ttk.Scrollbar(frm_list, orient='vertical', command=self.lst_monsters.yview)
        sb.pack(side='right', fill='y')
        self.lst_monsters.config(yscrollcommand=sb.set)
        self.lst_monsters.bind('<<ListboxSelect>>', lambda e: self.on_select())

        btn_frame = ttk.Frame(self, style="Custom.TFrame")
        btn_frame.pack(fill='x', pady=5)
        ttk.Button(btn_frame, text="➕ Ajouter au combat", style="Custom.TButton", command=self.add_to_tracker).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="➕ Nouveau monstre", style="Custom.TButton", command=self.new_monster_form).pack(side='left', padx=5)

        self.txt = tk.Text(self, height=15, font=("Consolas", 11), bg="white", fg="black")
        self.txt.pack(fill='both', expand=True, padx=10, pady=5)

        self.update_listbox()
        if self.filtered_names:
            self.lst_monsters.selection_set(0)
            self.show_stats(self.filtered_names[0])

    def on_search(self, *args):
        term = self.search_var.get().lower()
        self.filtered_names = [n for n in sorted(self.monsters) if term in n.lower()]
        self.update_listbox()
        if self.filtered_names:
            self.lst_monsters.selection_set(0)
            self.show_stats(self.filtered_names[0])
        else:
            self.txt.config(state='normal')
            self.txt.delete('1.0',tk.END)
            self.txt.config(state='disabled')

    def update_listbox(self):
        self.lst_monsters.delete(0, tk.END)
        for name in self.filtered_names:
            self.lst_monsters.insert(tk.END, name)

    def on_select(self):
        sel = self.lst_monsters.curselection()
        if sel:
            self.show_stats(self.filtered_names[sel[0]])

    def add_to_tracker(self):
        if not self.tracker:
            return
        sel = self.lst_monsters.curselection()
        if not sel:
            return
        data = self.monsters[self.filtered_names[sel[0]]]
        # Déléguer la création d'entité au système si disponible
        if self.system and hasattr(self.system, 'create_monster'):
            entity = self.system.create_monster(data)
        else:
            ac = data.get('ac')[0] if isinstance(data.get('ac'), list) else data.get('ac',0)
            hp = data.get('hp',{}).get('average') if isinstance(data.get('hp'), dict) else data.get('hp',0)
            cr = data.get('cr','0')
            entity = { 'name': data.get('name'), 'hp': hp, 'ac': ac, 'status':'', 'init':0,
                       'is_monster':True, 'challenge_rating':cr }
        self.tracker.add_entity_obj(entity)

    def show_stats(self, name):
        data = self.monsters.get(name,{})
        lines = []
        for key in ['name','source','page','size','type','alignment','cr']:
            if data.get(key) is not None:
                lines.append(f"{key.capitalize()}: {data.get(key)}")
        ac = data.get('ac')[0] if isinstance(data.get('ac'), list) else data.get('ac','')
        lines.append(f"CA: {ac}")
        hp = data.get('hp',{}).get('average') if isinstance(data.get('hp'), dict) else data.get('hp','')
        lines.append(f"PV: {hp}")
        # Stats
        stat_line = ' '.join(f"{s.upper()}:{data.get(s,'')}" for s in ['str','dex','con','int','wis','cha'] if data.get(s) is not None)
        if stat_line: lines.append(stat_line)
        # Vitesse
        sp = data.get('speed',{})
        if sp:
            sp_line = ' '.join(f"{k} {v}" for k,v in sp.items())
            lines.append(f"Vitesse: {sp_line}")
        # Autres champs
        for fld in ('skill','senses'):
            if data.get(fld): lines.append(f"{fld.capitalize()}: {data.get(fld)}")
        if data.get('hp') and isinstance(data['hp'], dict) and data['hp'].get('formula'):
            lines.append(f"Formule PV: {data['hp']['formula']}")
        # Affiche
        self.txt.config(state='normal')
        self.txt.delete('1.0',tk.END)
        self.txt.insert(tk.END, '\n'.join(lines))
        self.txt.config(state='disabled')
#
    def new_monster_form(self):
        # identique à avant, en fin d'ajout delegate à system.save_monster si disponible
        pass
