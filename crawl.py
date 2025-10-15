import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    async with AsyncWebCrawler() as crawler:
        categories = ["films", "series"]
        target_count = 510  # Nombre de titres à récupérer par catégorie

        for categorie in categories:
            print(f"Scraping la catégorie : {categorie}")
            titres_vus = set()
            page = 1

            while len(titres_vus) < target_count:
                url = f"https://www.justwatch.com/fr/{categorie}?page={page}"
                print(f" -> Page {page} : {url}")

                result = await crawler.arun(url=url)
                lignes = result.markdown.split("\n")

                for ligne in lignes:
                    ligne = ligne.strip()
                    if ligne and ligne not in titres_vus:
                        titres_vus.add(ligne)
                        if len(titres_vus) >= target_count:
                            break

                page += 1  # Passe à la page suivante

            # Sauvegarde des titres dans un fichier
            with open(f"{categorie}_510.txt", "w", encoding="utf-8") as f:
                for titre in list(titres_vus)[:target_count]:
                    f.write(titre + "\n")

            print(f"✅ {len(titres_vus)} titres de la catégorie '{categorie}' sauvegardés dans {categorie}_510.txt")

asyncio.run(main())