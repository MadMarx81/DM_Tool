import tkinter as tk
from tkinter import simpledialog, ttk

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

    def enter(self, event=None): self.schedule()
    def leave(self, event=None): self.unschedule(); self.hidetip()
    def schedule(self): self.unschedule(); self.id = self.widget.after(self.delay, self.showtip)
    def unschedule(self):
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = None
    def showtip(self):
        if self.tipwindow or not self.text: return
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += cy + self.widget.winfo_rooty() + 25
        tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = ttk.Label(
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

class InitiativeTracker(ttk.Frame):
    def __init__(self, master, system=None, **kwargs):
        super().__init__(master, **kwargs)
        self.system = system
        self.entities = []
        self.build_ui()

    def build_ui(self):
        frm_add = ttk.Frame(self)
        frm_add.pack(fill="x", pady=10)

        for i, txt in enumerate(["Nom", "PV", "CA", "État", "Init"]):
            ttk.Label(frm_add, text=txt).grid(row=0, column=i)

        self.e_name = ttk.Entry(frm_add, width=15)
        self.e_hp = ttk.Entry(frm_add, width=5)
        self.e_ac = ttk.Entry(frm_add, width=5)
        self.e_status = ttk.Entry(frm_add, width=10)
        self.e_init = ttk.Entry(frm_add, width=5)
        for idx, w in enumerate([self.e_name, self.e_hp, self.e_ac, self.e_status, self.e_init]):
            w.grid(row=1, column=idx)

        b_roll = ttk.Button(frm_add, text="🎲 Roll Init", command=self.roll_init)
        b_roll.grid(row=1, column=5, padx=5)
        Tooltip(b_roll, "Jette l'initiative via le système (1d20+mod)")

        b_add = ttk.Button(frm_add, text="➕ Ajouter", command=self.add_entity)
        b_add.grid(row=1, column=6, padx=5)
        Tooltip(b_add, "Ajoute l'entité au tracker")

        frm_list = ttk.Frame(self)
        frm_list.pack(fill="both", expand=True, padx=10, pady=10)
        titlebar = ttk.Label(
            frm_list,
            text="Init  |  Nom            |  PV  |  CA  |  État  | CR",
            font=("Georgia", 10, "bold"), anchor="w"
        )
        titlebar.pack(fill="x")

        self.lst = tk.Listbox(frm_list, font=("Consolas", 12))
        self.lst.pack(side="left", fill="both", expand=True)
        self.lst.bind('<Double-1>', self.edit_selected)
        sb = ttk.Scrollbar(frm_list, orient='vertical', command=self.lst.yview)
        sb.pack(side='right', fill='y')
        self.lst.config(yscrollcommand=sb.set)

        frm_ctrl = ttk.Frame(self)
        frm_ctrl.pack(fill='x', pady=5)
        for text, cmd in [
            ("🗑️ Suppr", self.delete_entity),
            ("🎲 Roll Sel", self.roll_selected),
            ("➖ Dégâts", self.apply_damage),
            ("➕ Soins", self.apply_heal)
        ]:
            btn = ttk.Button(frm_ctrl, text=text, command=cmd)
            btn.pack(side='left', padx=5)

    def roll_init(self):
        ent = self._read_entry(raw=True)
        if not ent or not self.system:
            self.e_init.delete(0, tk.END)
            return
        init_val = self.system.initiative(ent)
        self.e_init.delete(0, tk.END)
        self.e_init.insert(0, str(init_val))

    def _read_entry(self, raw=False):
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
        ent = {"name": name, "hp": hp, "ac": ac, "status": status, "init": init}
        if raw:
            return ent
        ent.update({
            "icon": "🧑‍💼",
            "is_monster": False,
            "challenge_rating": "0",
            "dex_mod": 0
        })
        return ent

    def add_entity(self):
        ent = self._read_entry()
        if not ent:
            return
        self.entities.append(ent)
        self.clear_entries()
        self.refresh()

    def add_entity_obj(self, entity):
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
        if not sel or not self.system:
            return
        idx = sel[0]
        ent = self.entities[idx]
        ent["init"] = self.system.initiative(ent)
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
            ttk.Label(dlg, text="État:").pack(padx=10, pady=5)
            var = tk.StringVar(value=ent['status'])
            combo = ttk.Combobox(dlg, textvariable=var, values=[], state='readonly')
            combo.pack(padx=10, pady=5)
            def on_ok():
                ent['status'] = var.get()
                dlg.destroy()
                self.refresh()
            ttk.Button(dlg, text="OK", command=on_ok).pack(pady=5)
            dlg.transient(self); dlg.grab_set(); self.wait_window(dlg)
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
