import tkinter as tk
from tkinter import ttk

class CustomGridViewPaned(ttk.Frame):

    def __init__(self, parent, rows=2, cols=2, available_views=None):
        super().__init__(parent)
        self.rows = rows
        self.cols = cols
        self.available_views = available_views or {}

        self.selected_views = {}

        self.paned_main = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned_main.pack(fill="both", expand=True)

        self.columns = []

        for col in range(cols):
            col_pane = tk.PanedWindow(self.paned_main, orient=tk.VERTICAL)
            self.paned_main.add(col_pane)
            self.columns.append(col_pane)

            for row in range(rows):
                frame = ttk.Frame(col_pane)
                col_pane.add(frame)

                # Fix taille minimale, taille expansion, poids etc.
                frame.rowconfigure(1, weight=1)  # 1 = index de content_frame, si on place les widgets en grid
                frame.columnconfigure(0, weight=1)

                selector = tk.StringVar()
                selector.set("Sélectionner une vue")

                menu = ttk.OptionMenu(
                    frame, selector, selector.get(),
                    *self.available_views.keys(),
                    command=lambda view_name, r=row, c=col: self.load_view(view_name, r, c)
                )
                menu.pack(fill="x")

                content_frame = ttk.Frame(frame)
                content_frame.pack(fill="both", expand=True)

                self.selected_views[(row, col)] = (selector, content_frame)

            # Ajuster la taille des panneaux verticaux dans la colonne
            # Donne une taille initiale égale aux panneaux (exemple)
            sizes = [int(100/rows)] * rows
            for i, size in enumerate(sizes):
                col_pane.paneconfigure(col_pane.panes()[i], minsize=50)  # taille min pour pas que ce soit trop petit

        # Ajuster la taille des colonnes dans la paned_main
        sizes = [int(100/cols)] * cols
        for i, size in enumerate(sizes):
            self.paned_main.paneconfigure(self.paned_main.panes()[i], minsize=100)

    def load_view(self, view_name, row, col):
        _, content_frame = self.selected_views[(row, col)]
        for widget in content_frame.winfo_children():
            widget.destroy()

        if view_name in self.available_views:
            view_class = self.available_views[view_name]
            view_instance = view_class(content_frame)
            view_instance.pack(fill="both", expand=True)
