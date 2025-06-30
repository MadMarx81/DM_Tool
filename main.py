import tkinter as tk

def main():
    # 1. Création de la fenêtre principale
    root = tk.Tk()
    root.title("DM Tool – Tableau de bord DnD")
    root.geometry("800x600")  # Taille par défaut

    # 2. Exemple de label de bienvenue
    welcome = tk.Label(root, text="Bienvenue dans DM Tool !", font=("Arial", 16))
    welcome.pack(pady=20)

    # 3. Lancement de la boucle principale
    root.mainloop()

if __name__ == "__main__":
    main()
