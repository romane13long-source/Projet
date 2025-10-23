import requests
import json
import time
from bs4 import BeautifulSoup

# --- Configuration ---
url = "https://apis.justwatch.com/graphql"
headers = {
    'accept': '*/*',
    'content-type': 'application/json',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

countries = ['FR', 'US', 'IT', 'DE', 'ES', 'GB', 'CA']
all_urls = []
seen_ids = set()
limit = 10
total_needed = 15

for country in countries:
    if len(all_urls) >= total_needed:
        break

    print(f"Pays: {country}")

    for offset in range(0, 2000, limit):
        if len(all_urls) >= total_needed:
            break

        payload = {
            'operationName': 'GetPopularTitles',
            'variables': {
                'first': limit,
                'offset': offset,
                'popularTitlesSortBy': 'POPULAR',
                'popularTitlesFilter': {'objectTypes': ['SHOW']},
                'language': 'fr',
                'country': country
            },
            'query': '''query GetPopularTitles($country: Country!, $first: Int!, $language: Language!, $offset: Int = 0, $popularTitlesFilter: TitleFilter, $popularTitlesSortBy: PopularTitlesSorting! = POPULAR) {
  popularTitles(country: $country, filter: $popularTitlesFilter, first: $first, sortBy: $popularTitlesSortBy, offset: $offset) {
    edges {
      node {
        id
        content(country: $country, language: $language) {
          fullPath
        }
      }
    }
  }
}'''
        }

        response = requests.post(url, headers=headers, json=payload)
        data = response.json()

        if 'data' in data and 'popularTitles' in data['data']:
            shows = data['data']['popularTitles']['edges']

            for show in shows:
                show_id = show['node']['id']
                if show_id not in seen_ids:
                    seen_ids.add(show_id)
                    full_path = show['node']['content']['fullPath']
                    full_url = f"https://www.justwatch.com{full_path}"
                    all_urls.append(full_url)

            print(f"Récupéré: {len(all_urls)} URLs uniques")

            if len(shows) < limit:
                break

      
for serie in all_urls:
    response = requests.get(serie)  
    content_html = response.text
    soup = BeautifulSoup(content_html, "html.parser")

    title_tag = soup.find("h1", class_="title-detail-hero_details_title")
    if title_tag:
        nom_film = title_tag.get_text(strip=True)
        print(f"Titre : {nom_film}")
    else:
        print("None")

    plateformes = soup.find_all("img", {"data-testid": "provider-icon-override"})
    if not plateformes:
        print("None")
    for p in plateformes:
        nom_plateforme = p.get("alt") or p.get("title")
        print(f"Série : {serie}")
        print(f"Plateforme : {nom_plateforme}")
        print("------------")
 
    duree = 