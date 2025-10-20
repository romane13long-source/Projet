import requests
import json
import time

url = "https://apis.justwatch.com/graphql"

headers = {
    'accept': '*/*',
    'content-type': 'application/json',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

countries = ['FR', 'US', 'IT', 'DE', 'ES', 'GB', 'CA']
all_movies = []
seen_ids = set()
limit = 40
total_needed = 5000

for country in countries:
    if len(all_movies) >= total_needed:
        break
    
    print(f"Pays: {country}")
    
    for offset in range(0, 2000, limit):
        if len(all_movies) >= total_needed:
            break
        
        payload = {
            'operationName': 'GetPopularTitles',
            'variables': {
                'first': limit,
                'offset': offset,
                'popularTitlesSortBy': 'POPULAR',
                'popularTitlesFilter': {
                    'objectTypes': ['MOVIE']
                },
                'language': 'fr',
                'country': country
            },
            'query': '''query GetPopularTitles($country: Country!, $first: Int!, $language: Language!, $offset: Int = 0, $popularTitlesFilter: TitleFilter, $popularTitlesSortBy: PopularTitlesSorting! = POPULAR) {
  popularTitles(country: $country, filter: $popularTitlesFilter, first: $first, sortBy: $popularTitlesSortBy, offset: $offset) {
    edges {
      node {
        id
        objectType
        content(country: $country, language: $language) {
          title
          fullPath
          originalReleaseYear
          shortDescription
          posterUrl
          scoring {
            imdbScore
            tmdbScore
          }
          genres {
            translation(language: $language)
          }
        }
      }
    }
  }
}'''
        }
        
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        
        if 'data' in data and 'popularTitles' in data['data']:
            movies = data['data']['popularTitles']['edges']
            
            for movie in movies:
                movie_id = movie['node']['id']
                if movie_id not in seen_ids:
                    seen_ids.add(movie_id)
                    all_movies.append(movie)
            
            print(f"Recupere: {len(all_movies)} films uniques")
            
            if len(movies) < limit:
                break
        
        time.sleep(1)

with open('justwatch_5000_films.json', 'w', encoding='utf-8') as f:
    json.dump(all_movies, f, indent=2, ensure_ascii=False)

print(f"Termine: {len(all_movies)} films sauvegardes dans justwatch_5000_films.json")