import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

NOTES_DIR = os.path.join("data", "notes")

class NotesView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.current_file = None

        os.makedirs(NOTES_DIR, exist_ok=True)

        # Layout principal : colonne gauche + éditeur
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # Colonne de gauche : liste des fichiers
        left_frame = ttk.Frame(self)
        left_frame.grid(row=0, column=0, sticky="ns")

        self.notes_listbox = tk.Listbox(left_frame, width=25)
        self.notes_listbox.pack(fill="y", expand=True)
        self.notes_listbox.bind("<<ListboxSelect>>", self.load_selected_note)

        ttk.Button(left_frame, text="➕ Nouvelle note", command=self.new_note).pack(fill="x")
        ttk.Button(left_frame, text="🗑️ Supprimer", command=self.delete_note).pack(fill="x")

        # Zone d’édition
        editor_frame = ttk.Frame(self)
        editor_frame.grid(row=0, column=1, sticky="nsew")

        self.text = ScrolledText(editor_frame, wrap="word", font=("Consolas", 11))
        self.text.pack(fill="both", expand=True)

        # Sauvegarde
        ttk.Button(editor_frame, text="💾 Sauvegarder", command=self.save_note).pack(anchor="e", padx=5, pady=5)

        self.refresh_note_list()

    def refresh_note_list(self):
        self.notes_listbox.delete(0, tk.END)
        for filename in sorted(os.listdir(NOTES_DIR)):
            if filename.endswith(".md"):
                self.notes_listbox.insert(tk.END, filename)

    def load_selected_note(self, event=None):
        selection = self.notes_listbox.curselection()
        if not selection:
            return
        filename = self.notes_listbox.get(selection[0])
        file_path = os.path.join(NOTES_DIR, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.current_file = file_path
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, content)

    def new_note(self):
        name = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown files", "*.md")],
            initialdir=NOTES_DIR,
            title="Créer une nouvelle note"
        )
        if name:
            with open(name, "w", encoding="utf-8") as f:
                f.write("# Nouvelle note\n\n")
            self.refresh_note_list()
            self.current_file = name
            self.load_note_from_path(name)

    def load_note_from_path(self, path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, content)

    def save_note(self):
        if self.current_file:
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(self.text.get(1.0, tk.END))
            messagebox.showinfo("Note sauvegardée", f"{os.path.basename(self.current_file)} sauvegardée.")
        else:
            messagebox.showwarning("Pas de fichier", "Aucune note sélectionnée pour la sauvegarde.")

    def delete_note(self):
        selection = self.notes_listbox.curselection()
        if not selection:
            return
        filename = self.notes_listbox.get(selection[0])
        file_path = os.path.join(NOTES_DIR, filename)
        if messagebox.askyesno("Confirmation", f"Supprimer {filename} ?"):
            os.remove(file_path)
            self.refresh_note_list()
            self.text.delete(1.0, tk.END)
            self.current_file = None
