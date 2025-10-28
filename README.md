# Projet
# =========================
# Récupération initiale
# =========================
- Accéder à la page principale du site
- Extraire les URL partielles de chaque film/série via JavaScript

# =========================
#  Reconstitution des URL complètes
# =========================
- Pour chaque URL partielle :
    - Ajouter le domaine principal pour créer l'URL complète
    
# =========================
# Extraction des informations
# =========================
- Charger le fichier JSON contenant les URL complètes
- Pour chaque URL :
    - Ouvrir la page correspondante
    - Récupérer le contenu HTML

# =========================
# Récupération des données depuis le HTML
# =========================
- Pour chaque page HTML :
    - Extraire le titre
    - Extraire le genre
    - Extraire l'année de sortie
    - Extraire les notes et avis
    - Extraire les plateformes disponibles
    - Extraire les réalisateurs et acteurs
    - Extraire toute autre information pertinente (durée, nombre de saisons, pays, etc.)

# =========================
# Stockage des données
# =========================
- Pour chaque film/série :
    - Créer un dictionnaire contenant toutes les informations extraites
    - Ajouter le dictionnaire à une liste globale
- En fin de scraping :
    - Sauvegarder la liste complète dans un fichier JSON
    - Sauvegarder la même liste dans un fichier CSV pour analyse

Pour exécuter le code, il faut taper python3 Final_code.py dans le terminal.
Celui-ci va scraper environ 6 500 films et séries, puis stocker les données dans un fichier JSON et un fichier CSV.
Le programme met environ quelques secondes à récupérer les informations de chaque film ou série.