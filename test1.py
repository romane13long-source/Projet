import requests
from bs4 import BeautifulSoup

full_url = ['https://www.justwatch.com/fr/film/demon-slayer-kimetsu-no-yaiba-infinity-castle', 'https://www.justwatch.com/fr/film/gone-girl']

# scraper les données de chaque url :

# Titre
for title in full_url:
    response = requests.get(full_url)
    content_html = response.text
    soup = BeautifulSoup(content_html, "html.parser")
    title = soup.find_all("h1", class_="title-detail-hero__details__title")

# Réalisateur
for producer in full_url:
    response = requests.get(full_url)
    content_html = response.text
    soup = BeautifulSoup(content_html, "html.parser")
    producer = soup.find_all("span", class_="title-credit-name")