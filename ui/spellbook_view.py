import tkinter as tk
import json
import os

class SpellbookView(tk.Frame):
    def __init__(self, master, data_dir="data/spells", **kwargs):
        super().__init__(master, **kwargs)
        self.data_dir = data_dir
        self.spells = self.load_spells()
        self.filtered_names = sorted(self.spells.keys())
        self.build_ui()

    def load_spells(self):
        spells = {}
        for filename in os.listdir(self.data_dir):
            if filename.endswith(".json"):
                path = os.path.join(self.data_dir, filename)
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for entry in data.get("spell", []):
                        name = entry.get("name")
                        if name:
                            spells[name] = entry
        return spells

    def build_ui(self):
        search_frame = tk.Frame(self)
        search_frame.pack(fill="x", pady=5)
        tk.Label(search_frame, text="🔍 Sort :").pack(side="left", padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.on_search)
        tk.Entry(search_frame, textvariable=self.search_var).pack(side="left", fill="x", expand=True)

        list_frame = tk.Frame(self)
        list_frame.pack(fill="both", expand=True, padx=10)
        self.lst = tk.Listbox(list_frame, height=12)
        self.lst.pack(side="left", fill="both", expand=True)
        self.lst.bind("<<ListboxSelect>>", lambda e: self.show_spell())
        sb = tk.Scrollbar(list_frame, orient="vertical", command=self.lst.yview)
        sb.pack(side="right", fill="y")
        self.lst.config(yscrollcommand=sb.set)

        self.txt = tk.Text(self, height=10, wrap="word", font=("Consolas", 10))
        self.txt.pack(fill="both", expand=True, padx=10, pady=5)

        self.update_list()

    def on_search(self, *args):
        term = self.search_var.get().lower()
        self.filtered_names = [name for name in self.spells if term in name.lower()]
        self.update_list()

    def update_list(self):
        self.lst.delete(0, tk.END)
        for name in self.filtered_names:
            self.lst.insert(tk.END, name)

    def show_spell(self):
        sel = self.lst.curselection()
        if not sel:
            return
        name = self.filtered_names[sel[0]]
        spell = self.spells.get(name, {})
        details = [f"Nom : {name}",
                   f"Niveau : {spell.get('level', '?')} | École : {spell.get('school', '?')}",
                   f"Temps d'incantation : {spell.get('time', [{}])[0].get('number', '')} {spell.get('time', [{}])[0].get('unit', '')}",
                   f"Portée : {spell.get('range', {}).get('distance', {}).get('amount', '')} {spell.get('range', {}).get('distance', {}).get('type', '')}",
                   f"Composants : {', '.join(k.upper() for k in spell.get('components', {}).keys())}",
                   "Effets :"]
        entries = spell.get("entries", [])
        for line in entries:
            details.append(f" - {line}")
        self.txt.config(state="normal")
        self.txt.delete("1.0", tk.END)
        self.txt.insert(tk.END, "\n".join(details))
        self.txt.config(state="disabled")
