import os
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from theme import setup_styles
from datetime import datetime

class PartyView(ttk.Frame):
    """
    Gère les personnages d’un groupe pour un système donné.
    """
    def __init__(
        self, parent,
        tracker=None,
        xp_calculator=None,
        log_view=None,
        system=None,
        **kwargs
    ):
        """
        :param tracker: InitiativeTracker
        :param xp_calculator: XPCombatCalculator
        :param log_view: CombatLogView
        :param system: instance de GameSystem définissant name(), compute_level(), etc.
        """
        setup_styles()
        super().__init__(parent, style="Custom.TFrame", **kwargs)
        self.tracker = tracker
        self.xp_calculator = xp_calculator
        self.log_view = log_view
        self.system = system

        # Répertoire des persos pour le système
        base = system.name() if system else "dnd5e"
        self.char_dir = os.path.join("data", base, "characters")
        os.makedirs(self.char_dir, exist_ok=True)

        # Layout triptyque
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)

        # GAUCHE: liste et contrôles
        left = ttk.Frame(self, style="Custom.TFrame")
        left.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        ttk.Label(left, text="🎭 Participants", style="Custom.TLabel").pack(pady=5)
        self.listbox = tk.Listbox(
            left, width=25, selectmode='extended',
            bg='#f9f7f0', fg='#5c4d3d', font=('Consolas',11)
        )
        self.listbox.pack(fill="both", expand=True, padx=5)
        self.listbox.bind("<<ListboxSelect>>", self.show_character_summary)

        btn_frame = ttk.Frame(left, style="Custom.TFrame")
        btn_frame.pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="➕ Nouveau", command=self.new_character, style="Custom.TButton").pack(fill="x", pady=2)
        ttk.Button(btn_frame, text="🗑️ Supprimer", command=self.delete_character, style="Custom.TButton").pack(fill="x", pady=2)
        ttk.Button(btn_frame, text="🚀 Importer", command=self.import_to_tracker, style="Custom.TButton").pack(fill="x", pady=2)

        # CENTRE: aperçu
        center = ttk.Frame(self, style="Custom.TFrame")
        center.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        ttk.Label(center, text="📋 Aperçu du personnage", style="Custom.TLabel").pack(pady=5)
        self.summary = tk.Text(
            center, bg='#f9f7f0', fg='#5c4d3d', font=('Consolas',11),
            state='disabled', wrap='word'
        )
        self.summary.pack(fill="both", expand=True, padx=5)

        # DROITE: formulaire
        right = ttk.Frame(self, style="Custom.TFrame")
        right.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        ttk.Label(right, text="✏️ Modifier / Ajouter", style="Custom.TLabel").grid(
            row=0, column=0, columnspan=2, pady=5
        )
        fields = [
            "name","hp_max","hp_current","ac","init_mod","dex_mod",
            "str","dex","con","int","wis","cha","status","xp"
        ]
        labels = [
            "Nom","PV Max","PV Actuels","CA","Mod Init","Mod DEX",
            "FOR","DEX","CON","INT","SAG","CHA","État","XP"
        ]
        self.vars = {}
        for i, (field, label) in enumerate(zip(fields, labels), start=1):
            ttk.Label(right, text=label+":", style="Custom.TLabel").grid(
                row=i, column=0, sticky="e", pady=2
            )
            var = tk.StringVar()
            entry = ttk.Entry(right, textvariable=var, style="Custom.TEntry")
            entry.grid(row=i, column=1, sticky="ew", pady=2)
            self.vars[field] = var
        right.columnconfigure(1, weight=1)
        ttk.Button(
            right, text="💾 Enregistrer", command=self.save_character, style="Custom.TButton"
        ).grid(row=len(fields)+1, column=0, columnspan=2, pady=10)

        self.current_file = None
        self.refresh()

    def refresh(self):
        """Recharge la liste des personnages"""
        self.listbox.delete(0, tk.END)
        for fname in sorted(os.listdir(self.char_dir)):
            if fname.endswith('.json'):
                self.listbox.insert(tk.END, fname)

    def new_character(self):
        """Vide le formulaire et le résumé"""
        self.current_file = None
        for var in self.vars.values(): var.set("")
        self.summary.config(state='normal')
        self.summary.delete('1.0', tk.END)
        self.summary.config(state='disabled')

    def show_character_summary(self, event=None):
        """Affiche résumé et charge formulaire"""
        sel = self.listbox.curselection()
        if not sel: return
        fname = self.listbox.get(sel[0])
        path = os.path.join(self.char_dir, fname)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except:
            return

        # Formulaire
        for field, var in self.vars.items():
            var.set(str(data.get(field, '')))

        # Niveau
        xp = data.get('xp', 0)
        lvl, to_next = (self.system.compute_level(xp) if self.system else (1,0))

        # Résumé
        summary_text = (
            f"Nom: {data.get('name','')}   Niveau: {lvl}\n"
            f"PV: {data.get('hp_current',0)}/{data.get('hp_max',0)}   CA: {data.get('ac',0)}   Init: {data.get('init_mod',0)}\n"
            f"Stats: FOR {data.get('str',0)}  DEX {data.get('dex',0)}  CON {data.get('con',0)}  "
            f"INT {data.get('int',0)}  SAG {data.get('wis',0)}  CHA {data.get('cha',0)}\n"
            f"État: {data.get('status','')}\n"
            f"XP: {xp}   → {to_next} XP avant niveau {lvl+1}\n"
        )
        self.summary.config(state='normal')
        self.summary.delete('1.0', tk.END)
        self.summary.insert(tk.END, summary_text)
        self.summary.config(state='disabled')

    def save_character(self):
        """Sauvegarde création ou mise à jour"""
        data = {}
        for field, var in self.vars.items():
            val = var.get().strip()
            if field in ('hp_max','hp_current','ac','init_mod','dex_mod',
                         'str','dex','con','int','wis','cha','xp'):
                try: data[field] = int(val)
                except: data[field] = 0
            else:
                data[field] = val
        if not data['name']:
            messagebox.showwarning("Nom manquant", "Le nom du personnage est requis.")
            return
        if not self.current_file:
            default = f"{data['name']}.json"
            path = filedialog.asksaveasfilename(
                defaultextension='.json', initialdir=self.char_dir,
                initialfile=default, filetypes=[('JSON','*.json')]
            )
            if not path: return
            self.current_file = path
        with open(self.current_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self.refresh()
        messagebox.showinfo("Enregistré", "Fiche sauvegardée.")

    def delete_character(self):
        """Supprime la fiche sélectionnée"""
        sel = self.listbox.curselection()
        if not sel: return
        fname = self.listbox.get(sel[0])
        if messagebox.askyesno("Supprimer", f"Supprimer {fname} ?"):
            os.remove(os.path.join(self.char_dir, fname))
            self.refresh()
            self.new_character()

    def log_combat(self, total_xp, monsters, players):
        """Ajoute une ligne dans le journal de combat"""
        if not self.log_view: return
        time_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        monster_names = ', '.join(m['name'] for m in monsters if m.get('hp',1)<=0)
        player_names = ', '.join(p['name'] for p in players)
        msg = f"[{time_str}] Combat: {monster_names} vaincus → {total_xp} XP répartis entre {player_names}"
        self.log_view.add_log(msg)

    def import_to_tracker(self):
        """Importe les personnages sélectionnés"""
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("Aucun sélection", "Sélectionnez au moins un personnage.")
            return
        if hasattr(self.tracker, 'clear_entities'):
            self.tracker.clear_entities(type='player')
        for idx in sel:
            fname = self.listbox.get(idx)
            with open(os.path.join(self.char_dir, fname), 'r', encoding='utf-8') as f:
                data = json.load(f)
            ent = self.system.create_player(data) if hasattr(self.system, 'create_player') else {
                'name': data['name'],
                'hp': data.get('hp_current', data.get('hp_max',0)),
                'ac': data.get('ac',0),
                'status': data.get('status',''),
                'init': data.get('init_mod',0),
                'is_monster': False,
                'challenge_rating':'0',
                'dex_mod': data.get('dex_mod',0)
            }
            self.tracker.add_entity_obj(ent)
        if hasattr(self.xp_calculator, 'calculate_xp'):
            self.xp_calculator.calculate_xp()
        self.show_character_summary()
        messagebox.showinfo("Import terminé", f"{len(sel)} persos ajoutés. XP mis à jour.")
