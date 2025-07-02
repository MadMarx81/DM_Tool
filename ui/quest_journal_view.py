import os
import json
import tkinter as tk
from tkinter import ttk, messagebox
from theme import BG_COLOR, LABEL_FG, ENTRY_BG, FONT_ENTRY, FONT_LABEL, FONT_BUTTON, setup_styles

# Répertoires
DATA_DIR = os.path.join("data")
QUEST_DIR = os.path.join(DATA_DIR, "quests")

# Statuts disponibles
STATUS_OPTIONS = ["En attente", "En cours", "Fini"]

class QuestJournalView(ttk.Frame):
    def __init__(self, parent):
        setup_styles()
        super().__init__(parent, style="Custom.TFrame")
        os.makedirs(QUEST_DIR, exist_ok=True)

        # Layout triptyque
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)

        # GAUCHE: liste et contrôles
        left = ttk.Frame(self, style="Custom.TFrame")
        left.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        ttk.Label(left, text="📜 Quêtes", style="Custom.TLabel").pack(pady=5)
        self.listbox = tk.Listbox(left, bg=ENTRY_BG, fg=LABEL_FG, font=FONT_ENTRY)
        self.listbox.pack(fill="both", expand=True, padx=5)
        self.listbox.bind('<<ListboxSelect>>', self.load_quest)
        btn_frame = ttk.Frame(left, style="Custom.TFrame")
        btn_frame.pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="➕ Nouveau", command=self.new_quest, style="Custom.TButton").pack(fill="x", pady=2)
        ttk.Button(btn_frame, text="✏️ Modifier", command=self.load_quest, style="Custom.TButton").pack(fill="x", pady=2)
        ttk.Button(btn_frame, text="💾 Enregistrer", command=self.save_quest, style="Custom.TButton").pack(fill="x", pady=2)
        ttk.Button(btn_frame, text="🗑️ Supprimer", command=self.delete_quest, style="Custom.TButton").pack(fill="x", pady=2)

        # CENTRE: aperçu
        center = ttk.Frame(self, style="Custom.TFrame")
        center.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        ttk.Label(center, text="🔍 Aperçu", style="Custom.TLabel").pack(pady=5)
        self.preview = tk.Text(center, bg=ENTRY_BG, fg=LABEL_FG, font=FONT_ENTRY,
                               state='disabled', wrap='word', relief='flat')
        self.preview.pack(fill="both", expand=True, padx=5)

        # DROITE: formulaire
        right = ttk.Frame(self, style="Custom.TFrame")
        right.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        ttk.Label(right, text="✏️ Détails / Création", style="Custom.TLabel").grid(
            row=0, column=0, columnspan=2, pady=5)
        # Champs
        fields = [
            ("name", "Nom"),
            ("giver", "Donneur"),
            ("location", "Lieu"),
            ("status", "Statut"),
            ("description", "Description")
        ]
        self.vars = {}  # pour StringVar et Combobox var
        self.texts = {}  # pour Text widgets
        for i, (key, label) in enumerate(fields, start=1):
            ttk.Label(right, text=label+":", style="Custom.TLabel").grid(
                row=i, column=0, sticky='e', pady=2, padx=2)
            if key == 'description':
                txt = tk.Text(right, bg=ENTRY_BG, fg=LABEL_FG, font=FONT_ENTRY,
                               height=5, relief='flat')
                txt.grid(row=i, column=1, sticky="ew", pady=2)
                self.texts[key] = txt
            elif key == 'status':
                var = tk.StringVar()
                cb = ttk.Combobox(right, textvariable=var, values=STATUS_OPTIONS, state='readonly', font=FONT_ENTRY)
                cb.grid(row=i, column=1, sticky="ew", pady=2)
                self.vars[key] = var
            else:
                var = tk.StringVar()
                entry = tk.Entry(right, textvariable=var, bg=ENTRY_BG, fg=LABEL_FG, font=FONT_ENTRY, relief='flat')
                entry.grid(row=i, column=1, sticky="ew", pady=2)
                self.vars[key] = var
        right.columnconfigure(1, weight=1)

        self.current = None
        self.refresh_list()

    def quest_path(self, name):
        safe = name.replace(' ', '_')
        return os.path.join(QUEST_DIR, f"{safe}.json")

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for fname in sorted(os.listdir(QUEST_DIR)):
            if fname.endswith('.json'):
                try:
                    with open(os.path.join(QUEST_DIR, fname), 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    display = data.get('name', fname[:-5])
                    self.listbox.insert(tk.END, display)
                    idx = self.listbox.size() - 1
                    status = data.get('status', 'En attente')
                    color = {'Fini':'green','En cours':'orange','En attente':'gray'}.get(status, LABEL_FG)
                    self.listbox.itemconfig(idx, fg=color)
                except:
                    continue
        # clear preview and form
        if not self.listbox.curselection():
            self.clear_form()

    def new_quest(self):
        self.clear_form()
        self.current = None

    def clear_form(self):
        # Vide formulaire et aperçu
        for key, var in self.vars.items():
            var.set(STATUS_OPTIONS[0] if key=='status' else "")
        for key, txt in self.texts.items():
            txt.delete('1.0', tk.END)
        self.preview.config(state='normal')
        self.preview.delete('1.0', tk.END)
        self.preview.config(state='disabled')

    def load_quest(self, event=None):
        sel = self.listbox.curselection()
        if not sel: return
        name = self.listbox.get(sel[0])
        path = self.quest_path(name)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger : {e}")
            return
        self.current = name
        # Remplir formulaire
        for key, var in self.vars.items():
            var.set(data.get(key, ''))
        for key, txt in self.texts.items():
            txt.delete('1.0', tk.END)
            txt.insert('1.0', data.get(key, ''))
        # Mettre à jour aperçu
        text = (
            f"Nom: {data.get('name','')}\n"
            f"Donneur: {data.get('giver','')}\n"
            f"Lieu: {data.get('location','')}\n"
            f"Statut: {data.get('status','')}\n\n"
            f"Description:\n{data.get('description','')}"
        )
        self.preview.config(state='normal')
        self.preview.delete('1.0', tk.END)
        self.preview.insert(tk.END, text)
        self.preview.config(state='disabled')

    def save_quest(self):
        name = self.vars['name'].get().strip()
        if not name:
            messagebox.showwarning("Nom requis", "Le nom de la quête est requis.")
            return
        data = {}
        for key, var in self.vars.items():
            data[key] = var.get().strip()
        for key, txt in self.texts.items():
            data[key] = txt.get('1.0', tk.END).strip()
        path = self.quest_path(name)
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Enregistré", f"Quête '{name}' enregistrée.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de sauvegarder : {e}")
        self.refresh_list()

    def delete_quest(self):
        sel = self.listbox.curselection()
        if not sel: return
        name = self.listbox.get(sel[0])
        if not messagebox.askyesno("Supprimer", "Supprimer cette quête ?"):
            return
        path = self.quest_path(name)
        try:
            os.remove(path)
            messagebox.showinfo("Supprimé", f"Quête '{name}' supprimée.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de supprimer : {e}")
        self.refresh_list()
