🧱 STRUCTURE DU PROJET

dnd_dashboard/
├── main.py                      # Point d’entrée de l’app Tkinter
├── ui/                          # Fichiers Tkinter par module
│   ├── initiative_tracker.py    # Interface de suivi des combats
│   ├── bestiary_view.py         # Affichage du bestiaire
│   ├── notes_view.py            # Carnet de notes markdown
│   └── wiki_view.py             # Wiki / règles maison
├── data/                        # Données brutes
│   ├── monsters/                # JSON de monstres
│   │   ├── goblin.json
│   │   ├── orc.json
│   │   └── ...
│   └── campaign_notes.md        # Notes de campagne en Markdown
├── logic/                       # Fonctions métier Python
│   ├── combat.py                # Gestion initiative, tri, dégâts
│   ├── bestiary.py              # Parsing JSON monstres
│   └── utils.py                 # Fonctions utilitaires
├── assets/                      # Icônes, images, etc. (facultatif)
├── README.md
└── requirements.txt             # Dépendances éventuelles

⚙️ FONCTIONNALITÉS PAR MODULE
🧠 1. Initiative Tracker

Ajouter PJ et PNJ avec Nom / Vie / CA / État / Initiative

Auto-roll init (1d20) ou saisie manuelle

Tri auto des entités par initiative décroissante

Boutons pour appliquer dégâts / soigner

    Suivi des statuts (empoisonné, étourdi, etc.)

🧟 2. Bestiaire

Chargement auto des fichiers JSON depuis data/monsters/

Interface pour rechercher/filtrer un monstre

Affichage : Nom, HP, CA, attaques, etc.

    (Option) Ajouter monstre sélectionné au tracker

📝 3. Carnet de notes (Markdown)

Chargement du fichier markdown

Édition de texte (zone de texte simple Tkinter)

    Sauvegarde au format .md

📚 4. Wiki / Règles

Pages éditables avec tableaux de règles

Format simple (HTML ou Markdown ? À définir)

    Peut servir de mémo MJ, liste d’effets, conditions, etc.

🛠️ MÉTHODOLOGIE & OUTILS
🧪 Versioning avec Git

Créer un dépôt Git local (git init)

Ajouter un .gitignore

Commit à chaque étape logique

    Bonus : création de branches pour fonctionnalités (ex. feature/initiative)

🧰 Outils et modules Python utiles

    tkinter → GUI

    json → Chargement bestiaire

    random → Pour les jets de dés

    markdown ou markdown2 (optionnel) → Rendu du carnet de notes

    os / glob → Explorer les fichiers JSON dans un dossier

🚀 FEUILLE DE ROUTE PROPOSÉE (par jalons)
✅ Étape 1 — Base du projet (0,5–1h)

    Créer les dossiers

    Fichier main.py avec fenêtre principale Tkinter

    Intégration Git (init, premier commit)

🎲 Étape 2 — Module initiative simple (2–3h)

    Ajouter un personnage avec nom / HP / init

    Auto-roll de l’initiative

    Tri + affichage

🧟 Étape 3 — Chargement du bestiaire JSON (2–3h)

    Créer quelques fichiers JSON de monstres simples

    Liste de sélection + affichage des données

❤️ Étape 4 — Suivi des PV / tour de combat (2–3h)

    Diminuer / augmenter HP

    Suivi de tour (qui joue, bouton "suivant")

📖 Étape 5 — Carnet de notes markdown (2–3h)

    Charger fichier texte

    Zone d’édition simple

    Sauvegarde sur modification

📚 Étape 6 — Wiki simplifié (facultatif/bonus)

    Rendu HTML / markdown en lecture seule

    Édition possible si envie plus tard

🤝 ET MOI DANS TOUT ÇA ?

Je te propose de procéder comme suit :

    Tu m’annonces quand tu veux commencer une étape.

    Je te propose un squelette ou un code de départ.

    Tu le testes, tu poses des questions, tu me dis si tu bloques.

    Tu commit régulièrement, et je peux même te faire relire des diff Git si tu veux progresser sur cet aspect.
