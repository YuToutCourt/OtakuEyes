import requests

from bs4 import BeautifulSoup
from anilist.anilist_api import get_id_by_name

WEB_SITE_TO_SCRAP = ["https://www.neko-sama.fr","https://animeresistance.stream"]

def scrap_main_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    all_anime = soup.find_all('div', class_='anime')
    for anime in all_anime:
        title = anime.find('div', class_='anime-title').text
        id = get_id_by_name(title)
        if id is None:
            continue
        episode = anime.find('div', class_='anime-episode').text
        yield id, episode

def get_all_new_episodes():
    all_anime = {scrap_main_page(url) for url in WEB_SITE_TO_SCRAP}

