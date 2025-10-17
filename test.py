import requests
import json
import time
import pandas as pd

# ============================================
# CONFIGURATION
# ============================================
TOTAL_FILMS = 150       # nombre total souhaité
BATCH_SIZE = 40         # films/séries par requête
DELAY = 1.5             # secondes entre requêtes
NUM_PAGES = (TOTAL_FILMS // BATCH_SIZE) + 1
COUNTRY = 'FR'          # pays
LANGUAGE = ['FR']       # langue pour la requête

# ============================================
# HEADERS
# ============================================
headers = {
    'accept': '*/*',
    'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    'app-version': '3.12.3-web-web',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'device-id': 'HsK2woR2w7bDukrCCMKPwq',
    'origin': 'https://www.justwatch.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.justwatch.com/',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
}

# ============================================
# PAYLOAD
# ============================================
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
            'objectTypes': ['MOVIE', 'SHOW'],
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
        'language': LANGUAGE,
        'country': COUNTRY
    },
    'query': '''
    query GetPopularTitles($country: Country!, $first: Int!, $language: Language!, $offset: Int!, $popularTitlesFilter: TitleFilter) {
      popularTitles(country: $country, filter: $popularTitlesFilter, first: $first, offset: $offset) {
        edges {
          node {
            objectType
            content(country: $country, language: $language) {
              title
              originalReleaseYear
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

# ============================================
# RÉCUPÉRATION DES PAGES
# ============================================
print("Récupération des pages...")
all_data = []

for page in range(NUM_PAGES):
    offset = page * BATCH_SIZE
    json_data['variables']['offset'] = offset
    print(f"Page {page + 1}/{NUM_PAGES} (offset {offset})...")

    try:
        response = requests.post('https://apis.justwatch.com/graphql', headers=headers, json=json_data)
        if response.status_code != 200:
            print(f"Erreur page {page+1}, status: {response.status_code}")
            continue
        data = response.json()
        if data.get('data', {}).get('popularTitles'):
            all_data.append(data)
    except Exception as e:
        print(f"Erreur page {page+1}: {e}")
    time.sleep(DELAY)

print(f"{len(all_data)} pages récupérées.\n")

# ============================================
# EXTRACTION DES INFORMATIONS
# ============================================
print("Extraction des infos...")
liste_films = []

for page_data in all_data:
    popular_titles = page_data.get('data', {}).get('popularTitles')
    if not popular_titles:
        continue
    edges = popular_titles.get('edges', [])

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
        realisateurs = ', '.join([c.get('name', '') for c in credits]) if credits else 'N/A'

        # Plateformes (toutes)
        offers = node.get('offers', []) or []
        plateformes = [offer.get('package', {}).get('clearName') for offer in offers if offer.get('package', {}).get('clearName')]
        # Mettre jusqu'à 3 colonnes
        plateforme1 = plateformes[0] if len(plateformes) > 0 else 'N/A'
        plateforme2 = plateformes[1] if len(plateformes) > 1 else 'N/A'
        plateforme3 = plateformes[2] if len(plateformes) > 2 else 'N/A'

        # Infos complètes
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
            'plateforme3': plateforme3
        }
        liste_films.append(infos_film)

print(f"{len(liste_films)} films/séries extraits.\n")

# ============================================
# SAUVEGARDE
# ============================================
# JSON
with open('films_propres.json', 'w', encoding='utf-8') as f:
    json.dump(liste_films, f, indent=2, ensure_ascii=False)

# CSV
df = pd.DataFrame(liste_films)
df.to_csv('films_justwatch.csv', index=False, encoding='utf-8')

print("Sauvegarde terminée :")
print("- JSON : films_propres.json")
print("- CSV  : films_justwatch.csv")
print(f"- Total : {len(liste_films)} films/séries")
