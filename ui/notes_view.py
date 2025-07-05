import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from theme import setup_styles

class NotesView(ttk.Frame):
    """
    Gestionnaire de notes pour un système générique.
    """
    def __init__(self, parent, system=None, **kwargs):
        """
        :param system: instance de GameSystem pour personnaliser le dossier
        """
        setup_styles()
        super().__init__(parent, style="Custom.TFrame", **kwargs)
        self.system = system
        base = system.name() if system else "dnd5e"
        self.notes_dir = os.path.join("data", base, "notes")
        os.makedirs(self.notes_dir, exist_ok=True)

        # Layout: liste à gauche, éditeur à droite
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # Liste des notes
        left_frame = ttk.Frame(self, style="Custom.TFrame")
        left_frame.grid(row=0, column=0, sticky="ns")
        ttk.Label(left_frame, text="📝 Notes", style="Custom.TLabel").pack(pady=5)
        self.listbox = tk.Listbox(
            left_frame, bg="#f9f7f0", fg="#5c4d3d", font=("Consolas",11)
        )
        self.listbox.pack(fill="y", expand=True)
        self.listbox.bind("<<ListboxSelect>>", self.load_selected_note)
        btn_frame = ttk.Frame(left_frame, style="Custom.TFrame")
        btn_frame.pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="➕ Nouvelle note", command=self.new_note, style="Custom.TButton").pack(fill="x", pady=2)
        ttk.Button(btn_frame, text="🗑️ Supprimer", command=self.delete_note, style="Custom.TButton").pack(fill="x", pady=2)

        # Éditeur
        editor = ttk.Frame(self, style="Custom.TFrame")
        editor.grid(row=0, column=1, sticky="nsew")
        self.text = ScrolledText(
            editor, bg="#f9f7f0", fg="#5c4d3d", font=("Consolas",11), wrap="word", relief='flat'
        )
        self.text.pack(fill="both", expand=True, padx=5, pady=5)
        ttk.Button(editor, text="💾 Sauvegarder", command=self.save_note, style="Custom.TButton").pack(anchor="e", padx=5, pady=5)

        self.current_file = None
        self.refresh_list()

    def refresh_list(self):
        """Recharge la liste des fichiers de notes"""
        self.listbox.delete(0, tk.END)
        for fname in sorted(os.listdir(self.notes_dir)):
            if fname.endswith('.md'):
                self.listbox.insert(tk.END, fname)

    def load_selected_note(self, event=None):
        """Charge la note sélectionnée dans l'éditeur"""
        sel = self.listbox.curselection()
        if not sel:
            return
        fname = self.listbox.get(sel[0])
        path = os.path.join(self.notes_dir, fname)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.current_file = path
        self.text.delete('1.0', tk.END)
        self.text.insert(tk.END, content)

    def new_note(self):
        """Crée une nouvelle note via un fichier Markdown"""
        path = filedialog.asksaveasfilename(
            defaultextension='.md', initialdir=self.notes_dir,
            initialfile='NewNote.md', filetypes=[('Markdown','*.md')]
        )
        if not path:
            return
        with open(path, 'w', encoding='utf-8') as f:
            f.write('# Nouvelle note\n\n')
        self.refresh_list()
        self.current_file = path
        self.text.delete('1.0', tk.END)
        self.text.insert(tk.END, '# Nouvelle note\n\n')

    def save_note(self):
        """Sauvegarde le contenu de l'éditeur dans le fichier courant"""
        if not self.current_file:
            messagebox.showwarning('Pas de fichier', 'Aucune note sélectionnée.')
            return
        with open(self.current_file, 'w', encoding='utf-8') as f:
            f.write(self.text.get('1.0', tk.END))
        messagebox.showinfo('Note sauvegardée', os.path.basename(self.current_file))
        self.refresh_list()

    def delete_note(self):
        """Supprime le fichier de note sélectionné"""
        sel = self.listbox.curselection()
        if not sel:
            return
        fname = self.listbox.get(sel[0])
        path = os.path.join(self.notes_dir, fname)
        if not messagebox.askyesno('Supprimer', f'Supprimer {fname} ?'):
            return
        os.remove(path)
        self.current_file = None
        self.text.delete('1.0', tk.END)
        self.refresh_list()
