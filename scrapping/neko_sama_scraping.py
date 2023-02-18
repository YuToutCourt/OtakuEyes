import logging
import os, re
import json
import difflib
import random
import requests

from bs4 import BeautifulSoup
from anime.anime import Anime, create_anime_object
from anilist.anilist_api import get_next_ep, get_id_by_name, retrive_anime

URL_JSON = "https://neko-sama.fr/animes-search-vostfr.json"

class NekoSamaScrapper:
    def __init__(self, url:str):
        self.url = url

    def scrap_main_page(self):
        """
        Return a list of anime object from the main page of neko_sama.fr 
        
        /!\ VF anime are not included
        """

        animes_list = []
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')
        all_anime = soup.find_all('a', class_='title')
        for anime in all_anime:
            str_anime = anime.text.split('Ep.')
            if "(VF)" in str_anime[0] : continue

            title, ep = str_anime[0], int(str_anime[1].strip())

            data = get_id_by_name(title)
            if data.get('errors') is not None: continue

            id = data.get('data').get('Media').get('id')
            anime_data = retrive_anime(id)

            if anime_data is None: continue

            anime_data['data']['Media']['episodes'] = ep
            print(anime_data)
            animes_list.append(create_anime_object(anime_data.get('data').get('Media')))

        return animes_list


    def get_json(self):
        """Return the json file from neko_sama.json"""

        # Get the json file
        if os.path.exists('neko_sama.json') and random.randint(0, 10) < 2:
            with open('neko_sama.json', 'r') as f:
                return json.load(f)
        else:
            r = requests.get(URL_JSON)
            with open('neko_sama.json', 'w') as f:
                json.dump(r.json(), f)
            return r.json()

    def find_anime_in_neko_sama(self, title_from_anilist:list[str]):
        """Return the anime from neko_sama.json that is the closest to the title from anilist"""
        data = self.get_json()
        for anime_name in title_from_anilist:
            try:
                # Get the anime title from neko_sama.json that is the closest to the title from anilist
                anime_name0 = difflib.get_close_matches(anime_name, [anime['title_english'] for anime in data], n=1, cutoff=0.6)
                anime_name1 = difflib.get_close_matches(anime_name, [anime['title'] if anime['title'] else "a" for anime in data], n=1, cutoff=0.6)
                anime_name2 = difflib.get_close_matches(anime_name, [anime['title_romanji'] if anime['title_romanji'] else "a" for anime in data], n=1, cutoff=0.6)

                list_of_final_anime_name = anime_name0 + anime_name1 + anime_name2

                anime_name = difflib.get_close_matches(anime_name, list_of_final_anime_name, n=1, cutoff=0.6)
                                                                    
            except Exception as e:
                logging.error(e)
                return None
        
            print(f"-----DEBUG :\nAnilist: {title_from_anilist}\nNeko Sama: {anime_name}\n-----")

            # If there is no anime that is close enough
            if len(anime_name) == 0: continue

            # Get the anime from neko_sama.json
            for anime in data:
                if anime_name[0] in [anime['title_english'], anime['title'], anime['title_romanji']]:
                    return anime
        
        else : return None

    def get_nb_episodes(self, anime:dict, id):
        """Return the number of episodes from neko_sama.json"""
        if anime['type'] == "m0v1e":
            return 1

        value = anime['nb_eps'].split(' ')[0]
        if value.isdigit():
            return int(value)

        ep = get_next_ep(id).get('data').get('Media').get('nextAiringEpisode')

        if ep is None:
            # If the number of episodes is unknown (ex: ?) use a default value of 100 episodes (it's enough)
            return 100
        
        return ep.get('episode') - 1 

    def get_video_url_of(self, anime:dict, episode:int):
        """Return the url of the episode from neko_sama.json"""

        url_episode = self.get_link_ep_anime(anime, episode)
        print(url_episode)
        r = requests.get(url_episode)
        soup = BeautifulSoup(r.text, 'lxml')

        # Don't ask me I have done black magic
        scripts = soup.find_all('script')

        for i, script in enumerate(scripts):
            # print('else' in script.text)
            if 'video' in script.text:
                s = scripts[i].text
                # print(s)
                index_= s.index('video')
                str_ = s[index_:index_+150]
                break
        else: return None

        # find the url in the string
        urls = re.findall(r'(https?://[^\s]+)', str_)

        if len(urls) == 0: return None

        for index, url in enumerate(urls):
            urls[index] = url.split("'")[0]

        return urls

    def get_link_ep_anime(self, anime:dict, episode:int):
        """Return all the episodes from neko_sama.json"""

        # Build url episode
        tmp_url = anime['url'].split('/')[-1].split('-')
        end_url = tmp_url[-1].split('_')
        end_url.insert(1,f'-{str(episode).zfill(2)}_')
        tmp_url[-1] = ''.join(end_url)
        print(tmp_url)
        url = '-'.join(tmp_url)

        return "https://www.neko-sama.fr/anime/episode/" + url
