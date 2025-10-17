import requests
import json
import time
import pandas as pd

# ============================================
# CONFIGURATION
# ============================================
NUM_PAGES = 10
DELAY = 1.5

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
    'sg': 'c=FR&l=fr&pv=f924f94f-51c3-421e-bab4-99aff8ffe2d3&d=HsK2woR2w7bDukrCCMKPwq&p=3.12.3-web-web&pa=%2Ffr',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
}

json_data = {
    'operationName': 'GetPopularTitles',
    'variables': {
        'first': 40,
        'popularTitlesSortBy': 'POPULAR',
        'sortRandomSeed': 0,
        'offset': 40,
        'creditsRole': 'DIRECTOR',
        'after': None,
        'popularTitlesFilter': {
            'ageCertifications': [],
            'excludeGenres': [],
            'excludeProductionCountries': [],
            'objectTypes': [],
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
        'country': 'FR',
    },
    'query': 'query GetPopularTitles($backdropProfile: BackdropProfile, $country: Country!, $first: Int! = 70, $format: ImageFormat, $language: Language!, $after: String, $popularTitlesFilter: TitleFilter, $popularTitlesSortBy: PopularTitlesSorting! = POPULAR, $profile: PosterProfile, $sortRandomSeed: Int! = 0, $watchNowFilter: WatchNowOfferFilter!, $offset: Int = 0, $creditsRole: CreditRole! = DIRECTOR) {\n  popularTitles(\n    country: $country\n    filter: $popularTitlesFilter\n    first: $first\n    sortBy: $popularTitlesSortBy\n    sortRandomSeed: $sortRandomSeed\n    offset: $offset\n    after: $after\n  ) {\n    __typename\n    edges {\n      cursor\n      node {\n        ...PopularTitleGraphql\n        __typename\n      }\n      __typename\n    }\n    pageInfo {\n      startCursor\n      endCursor\n      hasPreviousPage\n      hasNextPage\n      __typename\n    }\n    totalCount\n  }\n}\n\nfragment PopularTitleGraphql on MovieOrShow {\n  __typename\n  id\n  objectId\n  objectType\n  content(country: $country, language: $language) {\n    title\n    fullPath\n    originalReleaseYear\n    shortDescription\n    interactions {\n      likelistAdditions\n      dislikelistAdditions\n      __typename\n    }\n    scoring {\n      imdbVotes\n      imdbScore\n      tmdbPopularity\n      tmdbScore\n      tomatoMeter\n      certifiedFresh\n      jwRating\n      __typename\n    }\n    interactions {\n      votesNumber\n      __typename\n    }\n    dailymotionClips: clips(providers: [DAILYMOTION]) {\n      sourceUrl\n      externalId\n      provider\n      streamUrl\n      __typename\n    }\n    posterUrl(profile: $profile, format: $format)\n    ... on MovieOrShowOrSeasonContent {\n      backdrops(profile: $backdropProfile, format: $format) {\n        backdropUrl\n        __typename\n      }\n      __typename\n    }\n    isReleased\n    credits(role: $creditsRole) {\n      name\n      personId\n      __typename\n    }\n    runtime\n    genres {\n      translation(language: $language)\n      shortName\n      __typename\n    }\n    __typename\n  }\n  likelistEntry {\n    createdAt\n    __typename\n  }\n  dislikelistEntry {\n    createdAt\n    __typename\n  }\n  watchlistEntryV2 {\n    createdAt\n    __typename\n  }\n  customlistEntries {\n    createdAt\n    __typename\n  }\n  freeOffersCount: offerCount(\n    country: $country\n    platform: WEB\n    filter: {monetizationTypes: [FREE, ADS]}\n  )\n  watchNowOffer(country: $country, platform: WEB, filter: $watchNowFilter) {\n    ...WatchNowOffer\n    __typename\n  }\n  ... on Movie {\n    seenlistEntry {\n      createdAt\n      __typename\n    }\n    __typename\n  }\n  ... on Show {\n    tvShowTrackingEntry {\n      createdAt\n      __typename\n    }\n    seenState(country: $country) {\n      seenEpisodeCount\n      progress\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment WatchNowOffer on Offer {\n  __typename\n  id\n  standardWebURL\n  preAffiliatedStandardWebURL\n  streamUrl\n  streamUrlExternalPlayer\n  package {\n    id\n    icon\n    packageId\n    clearName\n    shortName\n    technicalName\n    iconWide(profile: S160)\n    hasRectangularIcon(country: $country, platform: WEB)\n    __typename\n  }\n  retailPrice(language: $language)\n  retailPriceValue\n  lastChangeRetailPriceValue\n  currency\n  presentationType\n  monetizationType\n  availableTo\n  dateCreated\n  newElementCount\n}\n',
}

response = requests.post('https://apis.justwatch.com/graphql', headers=headers, json=json_data)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"operationName":"GetPopularTitles","variables":{"first":40,"popularTitlesSortBy":"POPULAR","sortRandomSeed":0,"offset":40,"creditsRole":"DIRECTOR","after":null,"popularTitlesFilter":{"ageCertifications":[],"excludeGenres":[],"excludeProductionCountries":[],"objectTypes":[],"productionCountries":[],"subgenres":[],"genres":[],"packages":[],"excludeIrrelevantTitles":false,"presentationTypes":[],"monetizationTypes":[],"searchQuery":""},"watchNowFilter":{"packages":[],"monetizationTypes":[]},"language":"fr","country":"FR"},"query":"query GetPopularTitles($backdropProfile: BackdropProfile, $country: Country!, $first: Int! = 70, $format: ImageFormat, $language: Language!, $after: String, $popularTitlesFilter: TitleFilter, $popularTitlesSortBy: PopularTitlesSorting! = POPULAR, $profile: PosterProfile, $sortRandomSeed: Int! = 0, $watchNowFilter: WatchNowOfferFilter!, $offset: Int = 0, $creditsRole: CreditRole! = DIRECTOR) {\\n  popularTitles(\\n    country: $country\\n    filter: $popularTitlesFilter\\n    first: $first\\n    sortBy: $popularTitlesSortBy\\n    sortRandomSeed: $sortRandomSeed\\n    offset: $offset\\n    after: $after\\n  ) {\\n    __typename\\n    edges {\\n      cursor\\n      node {\\n        ...PopularTitleGraphql\\n        __typename\\n      }\\n      __typename\\n    }\\n    pageInfo {\\n      startCursor\\n      endCursor\\n      hasPreviousPage\\n      hasNextPage\\n      __typename\\n    }\\n    totalCount\\n  }\\n}\\n\\nfragment PopularTitleGraphql on MovieOrShow {\\n  __typename\\n  id\\n  objectId\\n  objectType\\n  content(country: $country, language: $language) {\\n    title\\n    fullPath\\n    originalReleaseYear\\n    shortDescription\\n    interactions {\\n      likelistAdditions\\n      dislikelistAdditions\\n      __typename\\n    }\\n    scoring {\\n      imdbVotes\\n      imdbScore\\n      tmdbPopularity\\n      tmdbScore\\n      tomatoMeter\\n      certifiedFresh\\n      jwRating\\n      __typename\\n    }\\n    interactions {\\n      votesNumber\\n      __typename\\n    }\\n    dailymotionClips: clips(providers: [DAILYMOTION]) {\\n      sourceUrl\\n      externalId\\n      provider\\n      streamUrl\\n      __typename\\n    }\\n    posterUrl(profile: $profile, format: $format)\\n    ... on MovieOrShowOrSeasonContent {\\n      backdrops(profile: $backdropProfile, format: $format) {\\n        backdropUrl\\n        __typename\\n      }\\n      __typename\\n    }\\n    isReleased\\n    credits(role: $creditsRole) {\\n      name\\n      personId\\n      __typename\\n    }\\n    runtime\\n    genres {\\n      translation(language: $language)\\n      shortName\\n      __typename\\n    }\\n    __typename\\n  }\\n  likelistEntry {\\n    createdAt\\n    __typename\\n  }\\n  dislikelistEntry {\\n    createdAt\\n    __typename\\n  }\\n  watchlistEntryV2 {\\n    createdAt\\n    __typename\\n  }\\n  customlistEntries {\\n    createdAt\\n    __typename\\n  }\\n  freeOffersCount: offerCount(\\n    country: $country\\n    platform: WEB\\n    filter: {monetizationTypes: [FREE, ADS]}\\n  )\\n  watchNowOffer(country: $country, platform: WEB, filter: $watchNowFilter) {\\n    ...WatchNowOffer\\n    __typename\\n  }\\n  ... on Movie {\\n    seenlistEntry {\\n      createdAt\\n      __typename\\n    }\\n    __typename\\n  }\\n  ... on Show {\\n    tvShowTrackingEntry {\\n      createdAt\\n      __typename\\n    }\\n    seenState(country: $country) {\\n      seenEpisodeCount\\n      progress\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\\nfragment WatchNowOffer on Offer {\\n  __typename\\n  id\\n  standardWebURL\\n  preAffiliatedStandardWebURL\\n  streamUrl\\n  streamUrlExternalPlayer\\n  package {\\n    id\\n    icon\\n    packageId\\n    clearName\\n    shortName\\n    technicalName\\n    iconWide(profile: S160)\\n    hasRectangularIcon(country: $country, platform: WEB)\\n    __typename\\n  }\\n  retailPrice(language: $language)\\n  retailPriceValue\\n  lastChangeRetailPriceValue\\n  currency\\n  presentationType\\n  monetizationType\\n  availableTo\\n  dateCreated\\n  newElementCount\\n}\\n"}'
#response = requests.post('https://apis.justwatch.com/graphql', headers=headers, data=data)
# ============================================
# PAYLOAD
# ============================================
json_data = {
    'operationName': 'GetPopularTitles',
    'variables': {
        'first': 40,
        'popularTitlesSortBy': 'POPULAR',
        'sortRandomSeed': 0,
        'offset': 0,
        'creditsRole': 'DIRECTOR',
        'after': None,
        'popularTitlesFilter': {
            'ageCertifications': [],
            'excludeGenres': [],
            'excludeProductionCountries': [],
            'objectTypes': [],
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
        'country': 'FR',
    },
    'query': 'query GetPopularTitles($backdropProfile: BackdropProfile, $country: Country!, $first: Int! = 70, $format: ImageFormat, $language: Language!, $after: String, $popularTitlesFilter: TitleFilter, $popularTitlesSortBy: PopularTitlesSorting! = POPULAR, $profile: PosterProfile, $sortRandomSeed: Int! = 0, $watchNowFilter: WatchNowOfferFilter!, $offset: Int = 0, $creditsRole: CreditRole! = DIRECTOR) {\n  popularTitles(\n    country: $country\n    filter: $popularTitlesFilter\n    first: $first\n    sortBy: $popularTitlesSortBy\n    sortRandomSeed: $sortRandomSeed\n    offset: $offset\n    after: $after\n  ) {\n    __typename\n    edges {\n      cursor\n      node {\n        ...PopularTitleGraphql\n        __typename\n      }\n      __typename\n    }\n    pageInfo {\n      startCursor\n      endCursor\n      hasPreviousPage\n      hasNextPage\n      __typename\n    }\n    totalCount\n  }\n}\n\nfragment PopularTitleGraphql on MovieOrShow {\n  __typename\n  id\n  objectId\n  objectType\n  content(country: $country, language: $language) {\n    title\n    fullPath\n    originalReleaseYear\n    shortDescription\n    interactions {\n      likelistAdditions\n      dislikelistAdditions\n      __typename\n    }\n    scoring {\n      imdbVotes\n      imdbScore\n      tmdbPopularity\n      tmdbScore\n      tomatoMeter\n      certifiedFresh\n      jwRating\n      __typename\n    }\n    interactions {\n      votesNumber\n      __typename\n    }\n    dailymotionClips: clips(providers: [DAILYMOTION]) {\n      sourceUrl\n      externalId\n      provider\n      streamUrl\n      __typename\n    }\n    posterUrl(profile: $profile, format: $format)\n    ... on MovieOrShowOrSeasonContent {\n      backdrops(profile: $backdropProfile, format: $format) {\n        backdropUrl\n        __typename\n      }\n      __typename\n    }\n    isReleased\n    credits(role: $creditsRole) {\n      name\n      personId\n      __typename\n    }\n    runtime\n    genres {\n      translation(language: $language)\n      shortName\n      __typename\n    }\n    __typename\n  }\n  likelistEntry {\n    createdAt\n    __typename\n  }\n  dislikelistEntry {\n    createdAt\n    __typename\n  }\n  watchlistEntryV2 {\n    createdAt\n    __typename\n  }\n  customlistEntries {\n    createdAt\n    __typename\n  }\n  freeOffersCount: offerCount(\n    country: $country\n    platform: WEB\n    filter: {monetizationTypes: [FREE, ADS]}\n  )\n  watchNowOffer(country: $country, platform: WEB, filter: $watchNowFilter) {\n    ...WatchNowOffer\n    __typename\n  }\n  ... on Movie {\n    seenlistEntry {\n      createdAt\n      __typename\n    }\n    __typename\n  }\n  ... on Show {\n    tvShowTrackingEntry {\n      createdAt\n      __typename\n    }\n    seenState(country: $country) {\n      seenEpisodeCount\n      progress\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment WatchNowOffer on Offer {\n  __typename\n  id\n  standardWebURL\n  preAffiliatedStandardWebURL\n  streamUrl\n  streamUrlExternalPlayer\n  package {\n    id\n    icon\n    packageId\n    clearName\n    shortName\n    technicalName\n    iconWide(profile: S160)\n    hasRectangularIcon(country: $country, platform: WEB)\n    __typename\n  }\n  retailPrice(language: $language)\n  retailPriceValue\n  lastChangeRetailPriceValue\n  currency\n  presentationType\n  monetizationType\n  availableTo\n  dateCreated\n  newElementCount\n}\n',
}

# ============================================
# ÉTAPE 1 : RÉCUPÉRER LES PAGES
# ============================================
print("Récupération des pages...")
all_data = []

for page in range(NUM_PAGES):
    offset = page * 40
    json_data['variables']['offset'] = offset
    
    print(f"Page {page + 1}/{NUM_PAGES} (offset: {offset})...")
    
    response = requests.post('https://apis.justwatch.com/graphql', headers=headers, json=json_data)
    data = response.json()
    all_data.append(data)
    
    time.sleep(DELAY)

print(f"{len(all_data)} pages récupérées\n")

# ============================================
# ÉTAPE 2 : EXTRAIRE LES INFOS DE CHAQUE FILM
# ============================================
print("Extraction des infos...")

# Liste pour stocker tous les films proprement
liste_films = []

# BOUCLE 1 : Sur chaque page
for page_data in all_data:
    
    # Récupérer les films de cette page
    films_de_cette_page = page_data['data']['popularTitles']['edges']
    
    # BOUCLE 2 : Sur chaque film de la page
    for film in films_de_cette_page:
        
        # Accéder aux infos du film
        node = film['node']
        content = node['content']
        
        # Récupérer les genres (c'est une liste, on la transforme en texte)
        liste_genres = []
        for genre in content.get('genres'):
            liste_genres.append(genre['translation'])
        genres_texte = ', '.join(liste_genres)
        
        # Créer un dictionnaire avec les infos qu'on veut
        infos_film = {
            'titre': content['title'],
            'annee': content['originalReleaseYear'],
            'description': content.get('shortDescription', 'N/A'),
            'note_imdb': content['scoring'].get('imdbScore'),
            'votes_imdb': content['scoring'].get('imdbVotes'),
            'note_jwrating': content['scoring'].get('jwRating'),
            'runtime': content.get('runtime'),
            'type': node['objectType'],
            'genres': genres_texte,
        }
        
        # Ajouter ce film à la liste
        liste_films.append(infos_film)

print(f"{len(liste_films)} films extraits\n")

# ============================================
# ÉTAPE 3 : SAUVEGARDER
# ============================================
print("Sauvegarde...")

# Sauvegarder en JSON
with open('films_propres.json', 'w') as file:
    json.dump(liste_films, file, indent=2, ensure_ascii=False)

print("Sauvegardé dans 'films_propres.json'")
print(f"\nIl y a {len(liste_films)} films")

# ============================================
# CONVERTIR EN CSV
# ============================================
# Créer un DataFrame pandas depuis ta liste de dictionnaires
df = pd.DataFrame(liste_films)

# Sauvegarder en CSV
df.to_csv('films_justwatch.csv', index=False, encoding='utf-8')

print("CSV créé : films_justwatch.csv")