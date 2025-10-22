import asyncio
import requests
from crawl4ai import AsyncWebCrawler
from bs4 import BeautifulSoup
import json
import pandas as pd

# =========================
# CONFIGURATION
# =========================
TOTAL_FILMS = 5
TOTAL_SERIES = 5
BATCH_SIZE = 5
DELAY = 1.5
COUNTRIES = ['FR', 'US', 'GB', 'DE', 'IT', 'ES', 'KO', 'JA', 'TR', 'PT']

headers = {
    'accept': '*/*',
    'content-type': 'application/json',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
}

# =========================
# FONCTION CRAWL SYNCHRONE
# =========================
def crawl_get(url: str):
    async def _run():
        async with AsyncWebCrawler() as crawler:
            return await crawler.arun(url=url)
    return asyncio.run(_run())

# =========================
# REQUÊTE GRAPHQL POUR FILMS / SERIES
# =========================
query = """
query GetPopularTitles($country: Country!, $first: Int!, $language: Language!, $offset: Int!, $popularTitlesFilter: TitleFilter) {
  popularTitles(country: $country, filter: $popularTitlesFilter, first: $first, offset: $offset) {
    edges {
      node {
        content(country: $country, language: $language) {
          fullPath
        }
      }
    }
  }
}
"""

# =========================
# FONCTION POUR RÉCUP URLS
# =========================
def get_urls(type_object, total):
    urls_set = set()
    for country in COUNTRIES:
        offset = 0
        while len(urls_set) < total:
            variables = {
                'country': country,
                'language': 'fr',
                'first': BATCH_SIZE,
                'offset': offset,
                'popularTitlesFilter': {'objectTypes': [type_object]}
            }
            response = requests.post(
                'https://apis.justwatch.com/graphql',
                headers=headers,
                json={'operationName': 'GetPopularTitles', 'variables': variables, 'query': query}
            )
            if response.status_code != 200:
                break
            data = response.json()
            edges = data.get('data', {}).get('popularTitles', {}).get('edges', [])
            if not edges:
                break
            for edge in edges:
                full_path = edge['node']['content'].get('fullPath')
                if full_path:
                    urls_set.add(f"https://www.justwatch.com{full_path}")
            offset += BATCH_SIZE
            if len(urls_set) >= total:
                break
    return list(urls_set)[:total]

# =========================
# FONCTION POUR SCRAPING INFOS
# =========================
def scrape_infos(urls, type_):
    result_list = []
    for url in urls:
        response = crawl_get(url)
        html_content = response.html
        soup = BeautifulSoup(html_content, "html.parser")

        # Plateformes
        plateformes = soup.find_all("img", {"data-testid": "provider-icon-override"})
        noms = [p.get("alt") or p.get("title") for p in plateformes]
        plateforme1 = noms[0] if len(noms) > 0 else None
        plateforme2 = noms[1] if len(noms) > 1 and noms[1] != plateforme1 else None
        plateforme3 = noms[2] if len(noms) > 2 and noms[2] not in (plateforme1, plateforme2) else None

        # Réalisateurs
        realisateurs = soup.find_all("span", class_="title-credit-name")
        noms_realisateurs = [r.get_text(strip=True) for r in realisateurs]

        # Nombre de saison
        if type_ == "SHOW":
            saison = soup.find("h2", class_="title-detail__title__text")
            saison_nb = saison.text.strip() if saison else None
        else:
            saison_nb = None

        # Durée
        infos = soup.find_all("div", class_="poster-detail-infos__value")
        duree_film = infos[7].text.strip() if type_ == "MOVIE" and len(infos) >= 8 else None

        # Dictionnaire final
        result_list.append({
            "url": url,
            "type": type_,
            "plateforme1": plateforme1,
            "plateforme2": plateforme2,
            "plateforme3": plateforme3,
            "realisateurs": noms_realisateurs,
            "nombre_saisons": saison_nb,
            "duree_film": duree_film
        })
    return result_list

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    # Récup URL
    films_urls = get_urls("MOVIE", TOTAL_FILMS)
    series_urls = get_urls("SHOW", TOTAL_SERIES)

    # Scraping
    films_data = scrape_infos(films_urls, "MOVIE")
    series_data = scrape_infos(series_urls, "SHOW")

    # Combiner tout
    all_data = films_data + series_data

    # Sauvegarde JSON
    with open("justwatch_data.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)

    # Sauvegarde CSV
    df = pd.DataFrame(all_data)
    df.to_csv("justwatch_data.csv", index=False, encoding="utf-8")

    print("✅ JSON et CSV sauvegardés !")
