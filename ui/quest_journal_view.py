#!/usr/bin/env python3

import os
import json
import tkinter as tk
from tkinter import ttk, messagebox
from theme import setup_styles

# Statuts disponibles
STATUS_OPTIONS = ["En attente", "En cours", "Fini"]

class QuestJournalView(ttk.Frame):
    """
    Gestionnaire de quêtes générique.
    """
    def __init__(self, parent, system=None, **kwargs):
        """
        :param system: GameSystem pour déterminer data/<system>/quests
        """
        setup_styles()
        super().__init__(parent, style="Custom.TFrame", **kwargs)
        self.system = system
        base = system.name() if system else "dnd5e"
        self.quest_dir = os.path.join("data", base, "quests")
        os.makedirs(self.quest_dir, exist_ok=True)

        # Layout triptyque
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)

        # GAUCHE: liste & contrôles
        left = ttk.Frame(self, style="Custom.TFrame")
        left.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        ttk.Label(left, text="📜 Quêtes", style="Custom.TLabel").pack(pady=5)
        self.listbox = tk.Listbox(
            left, bg="#f9f7f0", fg="#5c4d3d", font=("Consolas",11)
        )
        self.listbox.pack(fill="both", expand=True, padx=5)
        self.listbox.bind('<<ListboxSelect>>', self.load_quest)
        btn_frame = ttk.Frame(left, style="Custom.TFrame")
        btn_frame.pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="➕ Nouveau", command=self.new_quest, style="Custom.TButton").pack(fill="x", pady=2)
        ttk.Button(btn_frame, text="💾 Enregistrer", command=self.save_quest, style="Custom.TButton").pack(fill="x", pady=2)
        ttk.Button(btn_frame, text="🗑️ Supprimer", command=self.delete_quest, style="Custom.TButton").pack(fill="x", pady=2)

        # CENTRE: aperçu
        center = ttk.Frame(self, style="Custom.TFrame")
        center.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        ttk.Label(center, text="🔍 Aperçu", style="Custom.TLabel").pack(pady=5)
        self.preview = tk.Text(
            center, bg="#f9f7f0", fg="#5c4d3d", font=("Consolas",11),
            state='disabled', wrap='word', relief='flat'
        )
        self.preview.pack(fill="both", expand=True, padx=5)

        # DROITE: formulaire
        right = ttk.Frame(self, style="Custom.TFrame")
        right.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        ttk.Label(right, text="✏️ Détails / Création", style="Custom.TLabel").grid(
            row=0, column=0, columnspan=2, pady=5
        )
        fields = [
            ("name", "Nom"),
            ("giver", "Donneur"),
            ("location", "Lieu"),
            ("status", "Statut"),
            ("description", "Description")
        ]
        self.vars = {}
        self.texts = {}
        for i, (key, label) in enumerate(fields, start=1):
            ttk.Label(right, text=label+":", style="Custom.TLabel").grid(
                row=i, column=0, sticky='e', pady=2, padx=2
            )
            if key == 'description':
                txt = tk.Text(
                    right, bg="#f9f7f0", fg="#5c4d3d", font=("Consolas",11),
                    height=5, relief='flat', wrap='word'
                )
                txt.grid(row=i, column=1, sticky="ew", pady=2)
                self.texts[key] = txt
            elif key == 'status':
                var = tk.StringVar(value=STATUS_OPTIONS[0])
                cb = ttk.Combobox(
                    right, textvariable=var, values=STATUS_OPTIONS,
                    state='readonly', font=("Consolas",11)
                )
                cb.grid(row=i, column=1, sticky="ew", pady=2)
                self.vars[key] = var
            else:
                var = tk.StringVar()
                entry = tk.Entry(
                    right, textvariable=var,
                    bg="#f9f7f0", fg="#5c4d3d", font=("Consolas",11), relief='flat'
                )
                entry.grid(row=i, column=1, sticky="ew", pady=2)
                self.vars[key] = var
        right.columnconfigure(1, weight=1)

        self.current = None
        self.refresh_list()

    def quest_path(self, name):
        safe = name.replace(' ', '_')
        return os.path.join(self.quest_dir, f"{safe}.json")

    def refresh_list(self):
        """Recharge la liste et colore selon le statut"""
        self.listbox.delete(0, tk.END)
        for fname in sorted(os.listdir(self.quest_dir)):
            if not fname.endswith('.json'): continue
            path = os.path.join(self.quest_dir, fname)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                disp = data.get('name', fname[:-5])
                idx = self.listbox.size()
                self.listbox.insert(tk.END, disp)
                status = data.get('status', STATUS_OPTIONS[0])
                color = {'Fini':'green','En cours':'orange','En attente':'gray'}.get(status, '#5c4d3d')
                self.listbox.itemconfig(idx, fg=color)
            except:
                continue
        if not self.listbox.curselection():
            self.clear_form()

    def clear_form(self):
        """Vide formulaire et aperçu"""
        for key, var in self.vars.items():
            var.set(STATUS_OPTIONS[0] if key=='status' else "")
        for key, txt in self.texts.items():
            txt.delete('1.0', tk.END)
        self.preview.config(state='normal')
        self.preview.delete('1.0', tk.END)
        self.preview.config(state='disabled')
        self.current = None

    def new_quest(self):
        self.clear_form()

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
        for key, var in self.vars.items():
            var.set(data.get(key, ''))
        for key, txt in self.texts.items():
            txt.delete('1.0', tk.END)
            txt.insert('1.0', data.get(key, ''))
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
        """Enregistre ou met à jour la quête"""
        name = self.vars['name'].get().strip()
        if not name:
            messagebox.showwarning("Nom requis", "Le nom de la quête est requis.")
            return
        data = {key: var.get() for key, var in self.vars.items()}
        data.update({k: txt.get('1.0', tk.END).strip() for k, txt in self.texts.items()})
        path = self.quest_path(name)
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Enregistré", f"Quête '{name}' enregistrée.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de sauvegarder : {e}")
        self.refresh_list()

    def delete_quest(self):
        """Supprime la quête sélectionnée"""
        sel = self.listbox.curselection()
        if not sel: return
        name = self.listbox.get(sel[0])
        if not messagebox.askyesno("Supprimer", f"Supprimer la quête '{name}' ?"):
            return
        try:
            os.remove(self.quest_path(name))
            messagebox.showinfo("Supprimé", f"Quête '{name}' supprimée.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de supprimer : {e}")
        self.refresh_list()
