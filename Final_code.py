import asyncio
import requests
from crawl4ai import AsyncWebCrawler
from bs4 import BeautifulSoup
import json
import pandas as pd
import time

# =========================
# CONFIGURATION
# =========================
TOTAL_FILMS = 5000
TOTAL_SERIES = 5000
BATCH_SIZE = 40
DELAY = 1.5
COUNTRIES = ['FR', 'US', 'GB', 'IT', 'ES']

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
    for i, url in enumerate(urls, start=1):
        print(f" ({i}/{len(urls)}) Scraping {url}")
        try:
            response = crawl_get(url)
            html_content = response.html
            soup = BeautifulSoup(html_content, "html.parser")

            # Titre
            titre_tag = soup.find("h1", class_="title-detail-hero__details__title")

            titre = titre_tag[:-6] if len(titre_tag) > 6 else titre_tag
            titre = titre_tag.get_text(strip=True) if titre_tag else None      
            if titre_tag:
                titre = titre_tag.get_text(strip=True) 
                titre = titre[:-6] if len(titre) > 6 else titre  
            else:
                titre = "Titre inconnu"

            # Plateformes
            plateformes = soup.find_all("img", {"data-testid": "provider-icon-override"})
            noms = [p.get("alt") or p.get("title") for p in plateformes]
            plateforme1 = noms[0] if len(noms) > 0 else None
            plateforme2 = noms[1] if len(noms) > 1 and noms[1] != plateforme1 else None
            plateforme3 = noms[2] if len(noms) > 2 and noms[2] not in (plateforme1, plateforme2) else None

            # Récupérer tous les noms (réalisateurs + acteurs)
            all_credits = soup.find_all("span", class_="title-credit-name")
            noms_credits = [c.get_text(strip=True) for c in all_credits]

            # --- Séparer réalisateurs et acteurs ---
            limite_realisateurs = 3  
            noms_realisateurs = noms_credits[:limite_realisateurs] if noms_credits else []
            nom_acteurs = noms_credits[limite_realisateurs:] if len(noms_credits) > limite_realisateurs else []



            # Nombre de saison (pour séries)
            if type_ == "SHOW":
                saison = soup.find("h2", class_="title-detail__title__text")
                saison_nb = saison.text.strip() if saison else None
            else:
                saison_nb = None

            # Durée du film
            infos = soup.find_all("div", class_="poster-detail-infos__value")
            duree_film = infos[7].text.strip() if type_ == "MOVIE" and len(infos) >= 8 else None

            # Nombre d'avis
            nb_avis_tags = soup.find_all("span", class_="imdb-score")
            note_moyenne = [a.text.strip()[:3] for a in nb_avis_tags] if nb_avis_tags else []

            # Année de sortie
            balise_annee = soup.find_all("span", class_="release-year")
            annee = balise_annee[0].text.strip("()") if balise_annee else None

            # Genre
            genres = soup.find_all("div", class_="poster-detail-infos__value")
            genre_tag = genres[5].get_text(strip=True) if len(genres) >= 6 else None

            # Nombre de jours dans le top 100
            top100_tags = soup.find_all("p", class_="title-chart-info__item__value")
            top100 = top100_tags[2].text.strip()[:2] if len(top100_tags) >= 3 else None

            # Pays de production
            pays_tags = soup.find_all("div", class_="poster-detail-infos__value")
            pays = [tag.get_text(strip=True) for tag in pays_tags]
            pays_de_production = pays[-1] if len(pays) > 0 else None

            # Dictionnaire final
            result_list.append({
                "url": url,
                "type": type_,
                "titre": titre,
                "plateforme1": plateforme1,
                "plateforme2": plateforme2,
                "plateforme3": plateforme3,
                "realisateurs": noms_realisateurs,
                "acteurs": nom_acteurs,
                "nombre_saisons": saison_nb,
                "duree_film": duree_film,
                "note_moyenne": note_moyenne,
                "annee_sortie": annee,
                "genre": genre_tag,
                "jours_top100": top100,
                "pays_production": pays_de_production
            })

            # Petits points de progression visuelle
            if i % 5 == 0:
                print("...")

            time.sleep(DELAY)

        except Exception as e:
            print(f" Erreur sur {url}: {e}")
            continue

    return result_list

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    print(" Récupération des URLs des films...")
    films_urls = get_urls("MOVIE", TOTAL_FILMS)
    print(f" {len(films_urls)} URLs de films récupérées.")

    print(" Récupération des URLs des séries...")
    series_urls = get_urls("SHOW", TOTAL_SERIES)
    print(f"{len(series_urls)} URLs de séries récupérées.")

    print("Scraping des films...")
    films_data = scrape_infos(films_urls, "MOVIE")

    print("Scraping des séries...")
    series_data = scrape_infos(series_urls, "SHOW")

    # Combiner tout
    all_data = films_data + series_data

    # Sauvegarde JSON
    with open("justwatch_data.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)

    # Sauvegarde CSV
    df = pd.DataFrame(all_data)
    df.to_csv("justwatch_data.csv", index=False, encoding="utf-8")

    print(" Fichiers JSON et CSV sauvegardés avec succès !")
