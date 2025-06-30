import tkinter as tk
from tkinter import ttk
import json
import os

class BestiaryView(tk.Frame):
    def __init__(self, master, tracker=None, data_dir="data/monsters", **kwargs):
        super().__init__(master, **kwargs)
        self.tracker = tracker
        self.data_dir = data_dir
        self.monsters = self.load_monsters()
        self.filtered_names = sorted(self.monsters.keys())
        self.build_ui()

    def load_monsters(self):
        monsters = {}
        for filename in os.listdir(self.data_dir):
            if not filename.endswith('.json'):
                continue
            path = os.path.join(self.data_dir, filename)
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # JSON 5etools
                if isinstance(data, dict) and 'monster' in data and isinstance(data['monster'], list):
                    for entry in data['monster']:
                        name = entry.get('name')
                        if name:
                            monsters[name] = entry
                # JSON simple
                elif isinstance(data, dict) and 'name' in data:
                    monsters[data['name']] = data
        return monsters

    def build_ui(self):
        # Recherche
        frm_search = tk.Frame(self)
        frm_search.pack(fill='x', pady=5)
        tk.Label(frm_search, text="Chercher:").pack(side='left', padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace_add('write', self.on_search)
        tk.Entry(frm_search, textvariable=self.search_var).pack(side='left', fill='x', expand=True)

        # Liste des monstres filtrés
        frm_list = tk.Frame(self)
        frm_list.pack(fill='x', padx=10, pady=5)
        self.lst_monsters = tk.Listbox(frm_list, height=5)
        self.lst_monsters.pack(side='left', fill='x', expand=True)
        scrollbar = tk.Scrollbar(frm_list, orient='vertical', command=self.lst_monsters.yview)
        scrollbar.pack(side='right', fill='y')
        self.lst_monsters.config(yscrollcommand=scrollbar.set)
        self.lst_monsters.bind('<<ListboxSelect>>', lambda e: self.on_select())

        # Boutons
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill='x', pady=5)
        tk.Button(btn_frame, text="➕ Ajouter au combat", command=self.add_to_tracker).pack(side='left', padx=5)

        # Zone d'affichage des stats
        self.txt = tk.Text(self, width=60, height=15, state='disabled', font=('Consolas', 11))
        self.txt.pack(fill='both', expand=True, padx=10, pady=5)

        # Initialisation
        self.update_listbox()
        if self.filtered_names:
            self.lst_monsters.selection_set(0)
            self.show_stats(self.filtered_names[0])

    def on_search(self, *args):
        term = self.search_var.get().lower()
        self.filtered_names = [name for name in sorted(self.monsters.keys()) if name.lower().startswith(term)]
        self.update_listbox()
        if self.filtered_names:
            self.lst_monsters.selection_set(0)
            self.show_stats(self.filtered_names[0])
        else:
            self.txt.config(state='normal')
            self.txt.delete('1.0', tk.END)
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
        name = self.filtered_names[sel[0]]
        data = self.monsters[name]

        # Extraction CR
        cr = data.get('cr', '0')

        # Extraction CA
        ac_data = data.get('ac')
        if isinstance(ac_data, list):
            first = ac_data[0]
            ac = first.get('ac') if isinstance(first, dict) else first
        else:
            ac = ac_data or 0

        # Extraction HP
        hp_data = data.get('hp')
        if isinstance(hp_data, dict):
            hp = hp_data.get('average', 0)
        else:
            hp = hp_data or 0

        # Prépare l'entité avec challenge_rating
        entity = {
            "name": name,
            "hp": hp,
            "ac": ac,
            "status": "",
            "init": 0,
            "is_monster": True,
            "challenge_rating": cr
        }

        # Appelle la méthode d'ajout du tracker
        self.tracker.add_entity_obj(entity)

    def show_stats(self, name):
        data = self.monsters.get(name, {})

        # AC
        ac_data = data.get('ac')
        if isinstance(ac_data, list):
            first = ac_data[0]
            ac = first.get('ac') if isinstance(first, dict) else first
        else:
            ac = ac_data

        # HP
        hp_data = data.get('hp')
        if isinstance(hp_data, dict):
            hp = hp_data.get('average', '')
        else:
            hp = hp_data

        # CR
        cr = data.get('cr', '')

        # Attaques/Actions
        attacks = []
        for key in ('attacks', 'action'):
            if key in data and isinstance(data[key], list):
                attacks = data[key]
                break

        lines = [
            f"Nom: {name}",
            f"CR: {cr}",
            f"PV: {hp}",
            f"CA: {ac}",
            "Actions/Attaques:"
        ]
        for atk in attacks:
            if isinstance(atk, dict):
                title = atk.get('name', '')
                entries = atk.get('entries') or atk.get('damage', '')
                detail = ' '.join(entries) if isinstance(entries, list) else entries
                lines.append(f"  - {title}: {detail}")
            else:
                lines.append(f"  - {atk}")

        display = "\n".join(lines)
        self.txt.config(state='normal')
        self.txt.delete('1.0', tk.END)
        self.txt.insert(tk.END, display)
        self.txt.config(state='disabled')
