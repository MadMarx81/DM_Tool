import os
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Répertoire des fiches personnages
DATA_DIR = os.path.join("data")
CHAR_DIR = os.path.join(DATA_DIR, "characters")

class PartyView(ttk.Frame):
    def __init__(self, parent, tracker, xp_calculator):
        super().__init__(parent)
        self.tracker = tracker
        self.xp_calculator = xp_calculator
        os.makedirs(CHAR_DIR, exist_ok=True)

        # Configuration du layout
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # Colonne de gauche : liste des personnages
        left = ttk.Frame(self)
        left.grid(row=0, column=0, sticky="ns")
        ttk.Label(left, text="🎭 Participants", font=("Georgia", 11, "bold")).pack(pady=5)
        self.listbox = tk.Listbox(left, width=25)
        self.listbox.pack(fill="y", expand=True, padx=5)
        self.listbox.bind("<<ListboxSelect>>", self.load_character)

        btn_frame = ttk.Frame(left)
        btn_frame.pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="➕ Nouveau", command=self.new_character).pack(fill="x", pady=2)
        ttk.Button(btn_frame, text="🗑️ Supprimer", command=self.delete_character).pack(fill="x", pady=2)
        ttk.Button(btn_frame, text="🚀 Importer au combat", command=self.import_to_tracker).pack(fill="x", pady=2)

        # Colonne de droite : éditor fiche
        right = ttk.Frame(self)
        right.grid(row=0, column=1, sticky="nsew", padx=10)
        right.columnconfigure(1, weight=1)

        # Champs de fiche plus complets
        fields = [
            "name", "hp_max", "hp_current", "ac", "init_mod", "dex_mod",
            "str", "dex", "con", "int", "wis", "cha", "status"
        ]
        labels = [
            "Nom", "PV Max", "PV Actuels", "CA", "Mod Init", "Mod DEX",
            "FOR", "DEX", "CON", "INT", "SAG", "CHA", "État"
        ]
        self.vars = {}
        for i, (field, label) in enumerate(zip(fields, labels)):
            ttk.Label(right, text=label+":").grid(row=i, column=0, sticky="e", pady=2)
            var = tk.StringVar()
            entry = ttk.Entry(right, textvariable=var)
            entry.grid(row=i, column=1, sticky="ew", pady=2)
            self.vars[field] = var

        ttk.Button(right, text="💾 Enregistrer fiche", command=self.save_character).grid(
            row=len(fields), column=0, columnspan=2, pady=10
        )

        self.current_file = None
        self.refresh()

    def refresh(self):
        self.listbox.delete(0, tk.END)
        for fname in sorted(os.listdir(CHAR_DIR)):
            if fname.endswith('.json'):
                self.listbox.insert(tk.END, fname)

    def new_character(self):
        self.current_file = None
        for var in self.vars.values():
            var.set("")

    def load_character(self, event=None):
        sel = self.listbox.curselection()
        if not sel:
            return
        fname = self.listbox.get(sel[0])
        path = os.path.join(CHAR_DIR, fname)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.current_file = path
            for field, var in self.vars.items():
                var.set(str(data.get(field, '')))
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger {fname} : {e}")

    def save_character(self):
        data = {}
        for field, var in self.vars.items():
            val = var.get().strip()
            if field in ('hp_max','hp_current','ac','init_mod','dex_mod', 'str','dex','con','int','wis','cha'):
                try:
                    data[field] = int(val)
                except:
                    data[field] = 0
            else:
                data[field] = val
        if not data['name']:
            messagebox.showwarning("Nom manquant", "Le nom du personnage est requis.")
            return
        if not self.current_file:
            default = f"{data['name']}.json"
            path = filedialog.asksaveasfilename(
                defaultextension='.json', initialdir=CHAR_DIR,
                initialfile=default, filetypes=[('JSON','*.json')]
            )
            if not path:
                return
            self.current_file = path
        try:
            with open(self.current_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.refresh()
            messagebox.showinfo("Enregistré", "Fiche sauvegardée.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de sauvegarder : {e}")

    def delete_character(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        fname = self.listbox.get(sel[0])
        path = os.path.join(CHAR_DIR, fname)
        if messagebox.askyesno("Supprimer", f"Supprimer {fname} ?"):
            os.remove(path)
            self.refresh()
            self.new_character()

    def import_to_tracker(self):
        count = 0
        for fname in self.listbox.get(0, tk.END):
            path = os.path.join(CHAR_DIR, fname)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                entity = {
                    'name': data['name'],
                    'hp': data.get('hp_current', data.get('hp_max', 0)),
                    'ac': data['ac'],
                    'status': data.get('status',''),
                    'init': data.get('init_mod',0),
                    'is_monster': False,
                    'challenge_rating': '0',
                    'dex_mod': data.get('dex_mod',0)
                }
                self.tracker.add_entity_obj(entity)
                count += 1
            except:
                continue
        if hasattr(self.xp_calculator, 'set_player_count'):
            self.xp_calculator.set_player_count(count)
        messagebox.showinfo("Import terminé", f"{count} personnages ajoutés au combat.")
