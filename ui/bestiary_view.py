import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import json
import os

class BestiaryView(tk.Frame):
    CUSTOM_FILE = "custom_monsters.json"

    def __init__(self, master, tracker=None, data_dir="data/monsters", **kwargs):
        super().__init__(master, bg="#e6e2d3", **kwargs)
        self.tracker = tracker
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.custom_path = os.path.join(self.data_dir, self.CUSTOM_FILE)

        self.monsters = self.load_monsters()
        self.filtered_names = sorted(self.monsters.keys())
        self.build_ui()

    def load_monsters(self):
        monsters = {}
        for filename in os.listdir(self.data_dir):
            if not filename.endswith('.json') or filename == self.CUSTOM_FILE:
                continue
            path = os.path.join(self.data_dir, filename)
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict) and 'monster' in data and isinstance(data['monster'], list):
                    for entry in data['monster']:
                        name = entry.get('name')
                        if name:
                            monsters[name] = entry
                elif isinstance(data, dict) and 'name' in data:
                    monsters[data['name']] = data
        if os.path.exists(self.custom_path):
            with open(self.custom_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for entry in data.get('monster', []):
                    name = entry.get('name')
                    if name:
                        monsters[name] = entry
        return monsters

    def build_ui(self):
        frm_search = tk.Frame(self, bg="#e6e2d3")
        frm_search.pack(fill='x', pady=5)
        tk.Label(frm_search, text="Chercher:", bg="#e6e2d3", fg="#5c4d3d", font=("Georgia", 10)).pack(side='left', padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace_add('write', self.on_search)
        tk.Entry(frm_search, textvariable=self.search_var, bg="#f9f7f0").pack(side='left', fill='x', expand=True)

        frm_list = tk.Frame(self, bg="#e6e2d3")
        frm_list.pack(fill='x', padx=10, pady=5)
        self.lst_monsters = tk.Listbox(frm_list, height=6, bg="#fefcf5", font=("Consolas", 11))
        self.lst_monsters.pack(side='left', fill='x', expand=True)
        sb = tk.Scrollbar(frm_list, orient='vertical', command=self.lst_monsters.yview)
        sb.pack(side='right', fill='y')
        self.lst_monsters.config(yscrollcommand=sb.set)
        self.lst_monsters.bind('<<ListboxSelect>>', lambda e: self.on_select())

        btn_frame = tk.Frame(self, bg="#e6e2d3")
        btn_frame.pack(fill='x', pady=5)
        tk.Button(btn_frame, text="➕ Ajouter au combat", bg="#c9c2b8", command=self.add_to_tracker).pack(side='left', padx=5)
        tk.Button(btn_frame, text="➕ Nouveau monstre", bg="#c9c2b8", command=self.new_monster_form).pack(side='left', padx=5)

        self.txt = tk.Text(self, width=60, height=15, state='disabled', font=('Consolas',11), bg="#f9f7f0")
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
        stats = ['str','dex','con','int','wis','cha']
        stat_line = ' '.join(f"{s.upper()}:{data.get(s,'')}" for s in stats if data.get(s) is not None)
        if stat_line: lines.append(stat_line)
        sp = data.get('speed',{})
        if sp:
            sp_line = ' '.join(f"{k} {v}" for k,v in sp.items())
            lines.append(f"Vitesse: {sp_line}")
        if data.get('skill'): lines.append(f"Compétences: {data.get('skill')}")
        if data.get('senses'): lines.append(f"Sens: {data.get('senses')}")
        if data.get('hp') and isinstance(data['hp'], dict) and data['hp'].get('formula'):
            lines.append(f"Formule PV: {data['hp']['formula']}")
        display = '\n'.join(lines)
        self.txt.config(state='normal')
        self.txt.delete('1.0',tk.END)
        self.txt.insert(tk.END, display)
        self.txt.config(state='disabled')

    def new_monster_form(self):
        fields = [
            ('name','Nom'), ('source','Source'), ('page','Page'), ('size','Taille'),
            ('type','Type'), ('alignment','Alignement'), ('cr','CR'),
            ('ac','CA'), ('hp_avg','PV Moy'), ('hp_form','Formule PV'),
            ('speed','Vitesse (ex: walk=30,fly=60)'),
            ('str','FOR'), ('dex','DEX'), ('con','CON'),
            ('int','INT'), ('wis','SAG'), ('cha','CHA')
        ]

        win = tk.Toplevel(self, bg="#e6e2d3")
        win.title("Nouveau Monstre")
        vars_ = {}

        for i, (key, label) in enumerate(fields):
            tk.Label(win, text=label + ":", bg="#e6e2d3", fg="#5c4d3d").grid(row=i, column=0, sticky='e', padx=5, pady=2)
            var = tk.StringVar()
            tk.Entry(win, textvariable=var, bg="#f9f7f0").grid(row=i, column=1, sticky='ew', padx=5, pady=2)
            vars_[key] = var

        row_actions = len(fields)
        tk.Label(win, text="Actions (JSON list):", bg="#e6e2d3", fg="#5c4d3d").grid(row=row_actions, column=0, sticky='ne', padx=5, pady=2)
        txt_actions = ScrolledText(win, width=40, height=4, bg="#f9f7f0")
        txt_actions.grid(row=row_actions, column=1, padx=5, pady=2)

        def on_save():
            entry = {}
            entry['name'] = vars_['name'].get().strip()
            for num in ['page','cr','ac','hp_avg','str','dex','con','int','wis','cha']:
                try:
                    val = int(vars_[num].get())
                    if num == 'hp_avg':
                        entry['hp'] = val
                    else:
                        entry[num] = val
                except:
                    pass

            if 'hp' in entry:
                entry['hp'] = {'average': entry.pop('hp'), 'formula': vars_['hp_form'].get().strip()}

            sp = vars_['speed'].get().strip()
            if sp:
                d = {}
                for part in sp.split(','):
                    if '=' in part:
                        k, v = part.split('=')
                        try:
                            d[k.strip()] = int(v)
                        except:
                            pass
                if d:
                    entry['speed'] = d

            for textkey in ['source','size','type','alignment']:
                val = vars_[textkey].get().strip()
                if val:
                    entry[textkey] = [val] if textkey == 'size' else val

            raw = txt_actions.get("1.0", "end").strip()
            if raw:
                try:
                    actions = json.loads(raw)
                    if isinstance(actions, list):
                        entry['action'] = actions
                    else:
                        raise ValueError("Doit être une liste JSON")
                except Exception as e:
                    messagebox.showerror("JSON invalide", f"Impossible de parser les actions :\n{e}")
                    return

            if os.path.exists(self.custom_path):
                with open(self.custom_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {'monster': []}

            data['monster'].append(entry)
            with open(self.custom_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            win.destroy()
            self.monsters = self.load_monsters()
            self.filtered_names = sorted(self.monsters)
            self.update_listbox()
            messagebox.showinfo("Succès", f"{entry['name']} ajouté au bestiaire.")

        tk.Button(win, text="💾 Sauvegarder", command=on_save, bg="#c9c2b8") \
          .grid(row=row_actions+1, column=0, columnspan=2, pady=10)

        win.transient(self)
        win.grab_set()
        win.wait_window()
