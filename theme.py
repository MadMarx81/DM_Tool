# theme.py
"""
Centralisation des couleurs et styles pour DM_Tool.
"""

# Couleurs principales
BG_COLOR = "#e6e2d3"         # Fond général clair beige
LABEL_FG = "#5c4d3d"         # Brun doux pour les labels
ENTRY_BG = "#f9f7f0"         # Fond des entrées
BTN_BG = "#c9c2b8"           # Couleur sable clair pour les boutons
BTN_ACTIVE_BG = "#b8b09b"    # Couleur du bouton au survol
BTN_ACTIVE_FG = "#3e3428"    # Couleur du texte du bouton au survol

# Polices
FONT_LABEL = ("Georgia", 10)
FONT_ENTRY = ("Consolas", 11)
FONT_BUTTON = ("Georgia", 10)
FONT_RESULT = ("Georgia", 11, "italic")

# Configuration des styles ttk
def setup_styles():
    import tkinter.ttk as ttk
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Custom.TFrame", background=BG_COLOR)
    style.configure("Custom.TLabel", background=BG_COLOR, foreground=LABEL_FG, font=FONT_LABEL)
    style.configure("Custom.TButton", background=BTN_BG, foreground=LABEL_FG, font=FONT_BUTTON)
    style.map("Custom.TButton",
              background=[('active', BTN_ACTIVE_BG)],
              foreground=[('active', BTN_ACTIVE_FG)])
