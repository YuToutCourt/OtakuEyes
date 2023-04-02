import requests

from bs4 import BeautifulSoup
from anime.anime import Anime, create_anime_object
from anilist.anilist_api import get_id_by_name, retrive_anime

class AnimeResistanceScraper:
    def __init__(self, url):
        self.url = url

    def scrap_main_page(self):
        """
        Return a list of anime object from the main page of animeresistance.stream 
        
        /!\ VF anime are not included
        """

        animes_list = set()
        page = requests.get(self.url, verify=False)
        soup = BeautifulSoup(page.content, 'html.parser')
        all_anime = soup.find_all('div', class_='info')
        for anime in all_anime:
            str_anime = anime.text.split('EP.')
            str_anime[0] = str_anime[0].replace('\n', '')
            str_anime[1] = str_anime[1].replace('\n', '')
        
            if "(VF)" in str_anime[0] : continue

            title, ep = str_anime[0], int(float(str_anime[1].strip()))
            data = get_id_by_name(title)
            if data.get('errors') is not None: continue

            id = data.get('data').get('Media').get('id')
            anime_data = retrive_anime(id)

            if anime_data is None: continue

            anime_data['data']['Media']['episodes'] = ep
            animes_list.add(create_anime_object(anime_data.get('data').get('Media')))

        return animes_list