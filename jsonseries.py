import requests
import json
import time

# ============================================
# CONFIGURATION
# ============================================
TOTAL_SERIES = 5000       # Nombre de séries à récupérer
BATCH_SIZE = 40           # Séries par requête
DELAY = 1.5               # Temps entre les requêtes en secondes

# Liste des pays pour récupérer plus de séries
COUNTRIES = ['FR', 'US', 'GB', 'DE', 'IT']

# ============================================
# HEADERS
# ============================================
headers = {
    'accept': '*/*',
    'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    'app-version': '3.12.3-web-web',
    'content-type': 'application/json',
    'origin': 'https://www.justwatch.com',
    'referer': 'https://www.justwatch.com/',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
}

# ============================================
# FONCTION POUR RÉCUPÉRER LES SÉRIES D’UN PAYS
# ============================================
def fetch_series_for_country(country, total_needed):
    series = []
    offset = 0

    while len(series) < total_needed:
        json_data = {
            'operationName': 'GetPopularTitles',
            'variables': {
                'first': BATCH_SIZE,
                'popularTitlesSortBy': 'POPULAR',
                'sortRandomSeed': 0,
                'offset': offset,
                'creditsRole': 'DIRECTOR',
                'after': None,
                'popularTitlesFilter': {
                    'ageCertifications': [],
                    'excludeGenres': [],
                    'excludeProductionCountries': [],
                    'objectTypes': ['SHOW'],
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
            'query': '''query GetPopularTitles($country: Country!, $first: Int!, $language: Language!, $offset: Int!, $popularTitlesFilter: TitleFilter) {
                popularTitles(country: $country, filter: $popularTitlesFilter, first: $first, offset: $offset) {
                    edges {
                        node {
                            content(country: $country, language: $language) {
                                title
                                fullPath
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
                                    id
                                    technicalName
                                }
                                standardWebURL
                            }
                        }
                    }
                }
            }'''
        }

        try:
            response = requests.post('https://apis.justwatch.com/graphql', headers=headers, json=json_data)
            data = response.json()
            edges = data.get('data', {}).get('popularTitles', {}).get('edges', [])
            if not edges:
                break  # plus de séries disponibles
            series.extend(edges)
            print(f"{country}: récupérées {len(series)} séries")
        except Exception as e:
            print(f"Erreur pour {country} offset {offset}: {e}")
            break

        offset += BATCH_SIZE
        time.sleep(DELAY)

    return series[:total_needed]  # on ne garde que le nombre souhaité

# ============================================
# RÉCUPÉRATION DES SÉRIES
# ============================================
all_series = []

per_country = TOTAL_SERIES // len(COUNTRIES) + 1

for country in COUNTRIES:
    series_country = fetch_series_for_country(country, per_country)
    all_series.extend(series_country)
    if len(all_series) >= TOTAL_SERIES:
        break

all_series = all_series[:TOTAL_SERIES]

# ============================================
# SAUVEGARDE DU JSON BRUT
# ============================================
with open('series_brut.json', 'w', encoding='utf-8') as f:
    json.dump(all_series, f, indent=2, ensure_ascii=False)

print(f"\n✅ JSON brut sauvegardé : {len(all_series)} séries")
