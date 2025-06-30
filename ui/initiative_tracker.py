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
            font=("Arial", "10", "normal")
        )
        label.pack(ipadx=4, ipady=2)
        self.tipwindow = tw

    def hidetip(self):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

class InitiativeTracker(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.entities = []
        self.build_ui()

    def build_ui(self):
        frm_add = tk.Frame(self)
        frm_add.pack(fill="x", pady=10)
        # En-têtes
        for i, txt in enumerate(["Nom", "PV", "CA", "État", "Init"]):
            tk.Label(frm_add, text=txt, font=("Arial", 10, "bold")).grid(row=0, column=i)
        # Champs
        self.e_name = tk.Entry(frm_add, width=15)
        self.e_name.grid(row=1, column=0)
        self.e_hp = tk.Entry(frm_add, width=5)
        self.e_hp.grid(row=1, column=1)
        self.e_ac = tk.Entry(frm_add, width=5)
        self.e_ac.grid(row=1, column=2)
        self.e_status = tk.Entry(frm_add, width=10)
        self.e_status.grid(row=1, column=3)
        self.e_init = tk.Entry(frm_add, width=5)
        self.e_init.grid(row=1, column=4)
        # Boutons
        b_roll = tk.Button(frm_add, text="🎲 Roll Init", command=self.roll_init)
        b_roll.grid(row=1, column=5, padx=5)
        Tooltip(b_roll, "Jette 1d20 + mod DEX si fourni")
        b_add = tk.Button(frm_add, text="➕ Ajouter", command=self.add_entity)
        b_add.grid(row=1, column=6, padx=5)
        Tooltip(b_add, "Ajoute entité au tracker")

        # Listbox
        frm_list = tk.Frame(self)
        frm_list.pack(fill="both", expand=True, padx=10, pady=10)
        self.lst = tk.Listbox(frm_list, font=("Consolas", 12))
        self.lst.pack(side="left", fill="both", expand=True)
        self.lst.bind('<Double-1>', self.edit_selected)
        sb = tk.Scrollbar(frm_list, orient='vertical', command=self.lst.yview)
        sb.pack(side='right', fill='y')
        self.lst.config(yscrollcommand=sb.set)

        # Contrôles
        frm_ctrl = tk.Frame(self)
        frm_ctrl.pack(fill='x', pady=5)
        tk.Button(frm_ctrl, text="🗑️ Suppr", command=self.delete_entity).pack(side='left', padx=5)
        tk.Button(frm_ctrl, text="🎲 Roll Sel", command=self.roll_selected).pack(side='left', padx=5)
        tk.Button(frm_ctrl, text="➖ Dégâts", command=self.apply_damage).pack(side='left', padx=5)
        tk.Button(frm_ctrl, text="➕ Soins", command=self.apply_heal).pack(side='left', padx=5)

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
        ent = self._read_entry()
        if not ent:
            return
        self.entities.append(ent)
        self.clear_entries()
        self.refresh()

    def add_entity_obj(self, entity):
        # Fin de l'erreur AttributeError
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
        self.entities[idx]['hp'] -= amt  # PV peuvent devenir négatifs
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
        # Sélection champ
        field = simpledialog.askstring("Modifier","Champ (name,hp,init,status):", initialvalue="status")
        if not field or field not in ('name','hp','init','status'):
            return
        # Status avec Combobox
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
        # Numérique
        if field in ('hp','init'):
            val = simpledialog.askinteger("Modifier", f"Nouvelle valeur {field}:", initialvalue=ent[field], minvalue=0)
            if val is not None:
                ent[field] = val
                self.refresh()
            return
        # Name
        val = simpledialog.askstring("Modifier Nom", "Nouveau nom:", initialvalue=ent['name'])
        if val:
            ent['name'] = val
            self.refresh()

    def clear_entries(self):
        for w in (self.e_name, self.e_hp, self.e_ac, self.e_status, self.e_init):
            w.delete(0, tk.END)

    def refresh(self):
        self.entities.sort(key=lambda e: e.get('init', 0), reverse=True)
        self.lst.delete(0, tk.END)
        for i, e in enumerate(self.entities):
            self.lst.insert(
                tk.END,
                f"{e['init']:>3} • {e['name']:<12} HP:{e['hp']:<3} CA:{e['ac']:<2} [{e['status']}]"
            )
            if e['hp'] < 1:
                self.lst.itemconfig(i, fg='red')
