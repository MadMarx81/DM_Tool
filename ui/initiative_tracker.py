import tkinter as tk
from tkinter import simpledialog, ttk
import random

DND_STATES = [
    "Aveuglé", "Étourdi", "Empoisonné", "Paralysé",
    "Pétrifié", "Enflammé", "Gelé", "Inconscient",
    "Charmé", "Effrayé", "Renversé", "Restrained"
]

class Tooltip:
    """Ajoute un tooltip à un widget Tkinter."""
    def __init__(self, widget, text, delay=500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tipwindow = None
        self.id = None
        widget.bind('<Enter>', self.enter)
        widget.bind('<Leave>', self.leave)

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.delay, self.showtip)

    def unschedule(self):
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = None

    def showtip(self):
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += cy + self.widget.winfo_rooty() + 25
        tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            tw, text=self.text, justify=tk.LEFT,
            background="#ffffe0", relief=tk.SOLID, borderwidth=1,
            font=("Papyrus", "10", "normal")
        )
        label.pack(ipadx=4, ipady=2)
        self.tipwindow = tw

    def hidetip(self):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

class InitiativeTracker(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg="#e6e2d3", **kwargs)
        self.entities = []  # Liste d'entités (PJ et monstres)
        self.build_ui()

    def build_ui(self):
        # Cadre d'ajout
        frm_add = tk.Frame(self, bg="#e6e2d3")
        frm_add.pack(fill="x", pady=10)

        # En-têtes
        for i, txt in enumerate(["Nom", "PV", "CA", "État", "Init"]):
            tk.Label(frm_add, text=txt, font=("Georgia", 10, "bold"), bg="#e6e2d3", fg="#5c4d3d").grid(row=0, column=i)

        # Champs de saisie
        self.e_name = tk.Entry(frm_add, width=15, bg="#f9f7f0")
        self.e_name.grid(row=1, column=0)
        self.e_hp = tk.Entry(frm_add, width=5, bg="#f9f7f0")
        self.e_hp.grid(row=1, column=1)
        self.e_ac = tk.Entry(frm_add, width=5, bg="#f9f7f0")
        self.e_ac.grid(row=1, column=2)
        self.e_status = tk.Entry(frm_add, width=10, bg="#f9f7f0")
        self.e_status.grid(row=1, column=3)
        self.e_init = tk.Entry(frm_add, width=5, bg="#f9f7f0")
        self.e_init.grid(row=1, column=4)

        # Boutons
        b_roll = tk.Button(frm_add, text="🎲 Roll Init", command=self.roll_init, bg="#c9c2b8")
        b_roll.grid(row=1, column=5, padx=5)
        Tooltip(b_roll, "Jette 1d20 + mod DEX si fourni")
        b_add = tk.Button(frm_add, text="➕ Ajouter", command=self.add_entity, bg="#c9c2b8")
        b_add.grid(row=1, column=6, padx=5)
        Tooltip(b_add, "Ajoute entité au tracker")

        # Affichage du tracker
        frm_list = tk.Frame(self, bg="#e6e2d3")
        frm_list.pack(fill="both", expand=True, padx=10, pady=10)
        titlebar = tk.Label(frm_list, text="Init  |  Nom            |  PV  |  CA  |  État  | CR",
                            font=("Georgia", 10, "bold"), bg="#d6d1c4", anchor="w")
        titlebar.pack(fill="x")

        self.lst = tk.Listbox(frm_list, font=("Consolas", 12), bg="#fefcf5")
        self.lst.pack(side="left", fill="both", expand=True)
        self.lst.bind('<Double-1>', self.edit_selected)
        sb = tk.Scrollbar(frm_list, orient='vertical', command=self.lst.yview)
        sb.pack(side='right', fill='y')
        self.lst.config(yscrollcommand=sb.set)

        # Contrôles bas
        frm_ctrl = tk.Frame(self, bg="#e6e2d3")
        frm_ctrl.pack(fill='x', pady=5)
        for text, cmd in [
            ("🗑️ Suppr", self.delete_entity),
            ("🎲 Roll Sel", self.roll_selected),
            ("➖ Dégâts", self.apply_damage),
            ("➕ Soins", self.apply_heal)
        ]:
            btn = tk.Button(frm_ctrl, text=text, command=cmd, bg="#c9c2b8")
            btn.pack(side='left', padx=5)

    def roll_init(self):
        self.e_init.delete(0, tk.END)
        try:
            m = int(self.e_init.get())
        except ValueError:
            m = 0
        self.e_init.insert(0, str(random.randint(1, 20) + m))

    def _read_entry(self):
        try:
            name = self.e_name.get().strip()
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
        """Ajoute une nouvelle entité (PJ)."""
        ent = self._read_entry()
        if not ent:
            return
        ent.update({
            "icon": "🧑‍💼",
            "is_monster": False,
            "challenge_rating": "0",
            "dex_mod": 0
        })
        self.entities.append(ent)
        self.clear_entries()
        self.refresh()

    def add_entity_obj(self, entity):
        """Importe une entité (monstre ou PJ) depuis un dict externe."""
        entity.setdefault("icon", "🐉" if entity.get("is_monster") else "🧑‍💼")
        entity.setdefault("status", "")
        entity.setdefault("init", 0)
        entity.setdefault("is_monster", False)
        entity.setdefault("challenge_rating", "0")
        entity.setdefault("dex_mod", 0)
        self.entities.append(entity)
        self.refresh()

    def delete_entity(self):
        sel = self.lst.curselection()
        if sel:
            del self.entities[sel[0]]
            self.refresh()

    def roll_selected(self):
        sel = self.lst.curselection()
        if not sel:
            return
        idx = sel[0]
        ent = self.entities[idx]
        dex = ent.get('dex_mod', 0)
        ent['init'] = random.randint(1, 20) + dex
        self.refresh()

    def apply_damage(self):
        sel = self.lst.curselection()
        if not sel:
            return
        amt = simpledialog.askinteger("Dégâts", "Montant:", minvalue=0)
        if amt is None:
            return
        idx = sel[0]
        self.entities[idx]['hp'] -= amt
        self.refresh()

    def apply_heal(self):
        sel = self.lst.curselection()
        if not sel:
            return
        amt = simpledialog.askinteger("Soins", "Montant:", minvalue=0)
        if amt is None:
            return
        idx = sel[0]
        self.entities[idx]['hp'] += amt
        self.refresh()

    def edit_selected(self, event):
        sel = self.lst.curselection()
        if not sel:
            return
        idx = sel[0]
        ent = self.entities[idx]
        field = simpledialog.askstring("Modifier","Champ (name,hp,init,status):", initialvalue="status")
        if not field or field not in ('name','hp','init','status'):
            return
        if field == 'status':
            dlg = tk.Toplevel(self)
            dlg.title("Choisir état")
            tk.Label(dlg, text="État:").pack(padx=10, pady=5)
            var = tk.StringVar(value=ent['status'])
            combo = ttk.Combobox(dlg, textvariable=var, values=DND_STATES, state='readonly')
            combo.pack(padx=10, pady=5)
            def on_ok():
                ent['status'] = var.get()
                dlg.destroy()
                self.refresh()
            tk.Button(dlg, text="OK", command=on_ok).pack(pady=5)
            dlg.transient(self)
            dlg.grab_set()
            self.wait_window(dlg)
            return
        if field in ('hp','init'):
            val = simpledialog.askinteger("Modifier", f"Nouvelle valeur {field}:", initialvalue=ent[field], minvalue=0)
            if val is not None:
                ent[field] = val
                self.refresh()
            return
        val = simpledialog.askstring("Modifier Nom", "Nouveau nom:", initialvalue=ent['name'])
        if val:
            ent['name'] = val
            self.refresh()

    def clear_entries(self):
        for w in (self.e_name, self.e_hp, self.e_ac, self.e_status, self.e_init):
            w.delete(0, tk.END)

    def refresh(self):
        # Tri par initiative décroissante
        self.entities.sort(key=lambda e: e.get('init', 0), reverse=True)
        self.lst.delete(0, tk.END)
        for i, e in enumerate(self.entities):
            icon = e.get('icon', '🐉' if e.get('is_monster') else '🧑‍💼')
            line = (
                f"{e.get('init',0):>3} • {icon} {e['name']:<12} "
                f"HP:{e['hp']:<3} CA:{e['ac']:<2} [{e.get('status','')}]"
            )
            if e.get('is_monster'):
                line += f"  (CR {e.get('challenge_rating','')})"
            self.lst.insert(tk.END, line)
            if e['hp'] < 1:
                self.lst.itemconfig(i, fg='red')

