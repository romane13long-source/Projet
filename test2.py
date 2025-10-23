import requests
from bs4 import BeautifulSoup
all_urls = ['https://www.justwatch.com/fr/film/demon-slayer-kimetsu-no-yaiba-infinity-castle', 'https://www.justwatch.com/fr/film/gone-girl']
# scraper les données de chaque url :

for serie in all_urls:
    response = requests.get(serie, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    plateformes = soup.find_all("img", {"data-testid": "provider-icon-override"})
    for plateforme in plateformes:
        nom_plateforme = plateforme.get("alt") or plateforme.get("title")
        print(f"Série : {serie}")
        print(f"Plateforme : {nom_plateforme}\n")

