import requests
import json
import time
import pandas as pd

# ============================================
# CONFIGURATION
# ============================================
TOTAL_FILMS = 15000     # nombre total souhaité
BATCH_SIZE = 40         # films par requête
DELAY = 1.5             # secondes entre requêtes

# Liste des pays à scraper
COUNTRIES = ['FR', 'US', 'GB', 'DE', 'IT', 'ES', 'KO', 'JA', 'TR', 'PT']

# ============================================
# HEADERS
# ============================================
headers = {
    'accept': '*/*',
    'accept-language': 'fr-FR,fr;q=0.9',
    'app-version': '3.12.3-web-web',
    'content-type': 'application/json',
    'origin': 'https://www.justwatch.com',
    'referer': 'https://www.justwatch.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
}

# ============================================
# ÉTAPE 1 : RÉCUPÉRATION DES PAGES
# ============================================
all_data = []

for country in COUNTRIES:
    films_par_pays = TOTAL_FILMS // len(COUNTRIES)
    num_pages = (films_par_pays // BATCH_SIZE) + 1
    print(f"\nRécupération des pages pour {country}...")
    
    json_data = {
        'operationName': 'GetPopularTitles',
        'variables': {
            'first': BATCH_SIZE,
            'popularTitlesSortBy': 'POPULAR',
            'sortRandomSeed': 0,
            'offset': 0,
            'creditsRole': 'DIRECTOR',
            'after': None,
            'popularTitlesFilter': {
                'ageCertifications': [],
                'excludeGenres': [],
                'excludeProductionCountries': [],
                'objectTypes': ['MOVIE'],  # films uniquement
                'productionCountries': [],
                'subgenres': [],
                'genres': [],
                'packages': [],
                'excludeIrrelevantTitles': False,
                'presentationTypes': [],
                'monetizationTypes': [],
                'searchQuery': '',
            },
            'watchNowFilter': {
                'packages': [],
                'monetizationTypes': [],
            },
            'language': 'fr',
            'country': country,
        },
        'query': '''
        query GetPopularTitles($country: Country!, $first: Int!, $language: Language!, $offset: Int!, $popularTitlesFilter: TitleFilter) {
          popularTitles(country: $country, filter: $popularTitlesFilter, first: $first, offset: $offset) {
            edges {
              node {
                id
                objectType
                content(country: $country, language: $language) {
                  title
                  originalReleaseYear
                  shortDescription
                  runtime
                  scoring {
                    imdbScore
                    imdbVotes
                    jwRating
                  }
                  genres {
                    translation(language: $language)
                  }
                  credits(role: DIRECTOR) {
                    name
                  }
                }
                offers(country: $country, platform: WEB) {
                  package {
                    clearName
                  }
                }
              }
            }
          }
        }
        '''
    }

    for page in range(num_pages):
        offset = page * BATCH_SIZE
        json_data['variables']['offset'] = offset

        print(f"  Page {page + 1}/{num_pages} (offset: {offset})...")
        try:
            response = requests.post('https://apis.justwatch.com/graphql', headers=headers, json=json_data)
            data = response.json()
            # On ne stocke que si data et popularTitles existent
            if data and data.get('data') and data['data'].get('popularTitles'):
                all_data.append(data)
        except Exception as e:
            print(f"⚠️ Erreur sur la page {page + 1}: {e}")
        time.sleep(DELAY)

print(f"\n{len(all_data)} pages récupérées ✅\n")

# ============================================
# ÉTAPE 2 : EXTRACTION DES INFORMATIONS
# ============================================
print("Extraction des infos...")

liste_films = []

for page_data in all_data:
    # Sécurité : ne pas essayer de get si page_data est None
    if not page_data or not page_data.get('data') or not page_data['data'].get('popularTitles'):
        continue

    edges = page_data['data']['popularTitles'].get('edges', [])
    for film in edges:
        node = film.get('node', {})
        content = node.get('content', {})
        if not content:
            continue

        # Genres
        genres = [g.get('translation', '') for g in content.get('genres', [])]
        genres_texte = ', '.join(genres)

        # Réalisateurs
        credits = content.get('credits', [])
        realisateurs = ', '.join([c.get('name') for c in credits]) if credits else 'N/A'

        # Plateformes (plusieurs possibles)
        offers = node.get('offers', []) or []
        plateformes = [offer.get('package', {}).get('clearName') for offer in offers if offer.get('package', {}).get('clearName')]
        # Jusqu'à 3 plateformes
        plateforme1 = plateformes[0] if len(plateformes) > 0 else 'N/A'
        plateforme2 = plateformes[1] if len(plateformes) > 1 else 'N/A'
        plateforme3 = plateformes[2] if len(plateformes) > 2 else 'N/A'

        # Infos du film
        infos_film = {
            'titre': content.get('title', 'N/A'),
            'annee': content.get('originalReleaseYear', 'N/A'),
            'note_imdb': content.get('scoring', {}).get('imdbScore'),
            'votes_imdb': content.get('scoring', {}).get('imdbVotes'),
            'type': node.get('objectType', 'N/A'),
            'genres': genres_texte,
            'realisateurs': realisateurs,
            'plateforme1': plateforme1,
            'plateforme2': plateforme2,
            'plateforme3': plateforme3,
        }

        liste_films.append(infos_film)

print(f"{len(liste_films)} films extraits ✅\n")

# ============================================
# ÉTAPE 3 : SAUVEGARDE
# ============================================
print("Sauvegarde...")

with open('films_propres.json', 'w', encoding='utf-8') as f:
    json.dump(liste_films, f, indent=2, ensure_ascii=False)

df = pd.DataFrame(liste_films)
df.to_csv('films_justwatch.csv', index=False, encoding='utf-8')

print("✅ Sauvegarde terminée :")
print(f"- JSON : films_propres.json")
print(f"- CSV  : films_justwatch.csv")
print(f"- Total : {len(liste_films)} films\n")
