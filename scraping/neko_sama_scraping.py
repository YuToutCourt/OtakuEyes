import re
import json
import difflib
import requests

from bs4 import BeautifulSoup
from anime.anime import create_anime_object
from anilist.anilist_api import get_next_ep, get_id_by_name, retrive_anime
from icecream import ic

# URL_JSON = "https://neko-sama.fr/animes-search-vostfr.json"
URL_JSON = "https://185.146.232.127/animes-search-vostfr.json"

class NekoSamaScraper:
    def __init__(self, url:str):
        self.url = url

    def scrap_main_page(self):
        """
        Return a list of anime object from the main page of neko_sama.fr 
        
        /!\ VF anime are not included
        """

        animes_list = set()
        page = requests.get(self.url, verify=False)
        soup = BeautifulSoup(page.content, 'html.parser')
        all_anime = soup.find_all('a', class_='title')
        for anime in all_anime:
            str_anime = anime.text.split('Ep.')
            if "(VF)" in str_anime[0] : continue

            title, ep = str_anime[0], int(float(str_anime[1].strip()))

            data = get_id_by_name(title)
            if data.get('errors') is not None: continue

            id = data.get('data').get('Media').get('id')
            anime_data = retrive_anime(id)

            if anime_data is None: continue

            anime_data['data']['Media']['episodes'] = ep
            animes_list.add(create_anime_object(anime_data.get('data').get('Media')))

        ic(animes_list)
        return animes_list

    def get_json(self):
        """Return the json file from neko_sama.json"""

        # Get the json file
        r = requests.get(URL_JSON, verify=False)
        with open('neko_sama.json', 'w') as f:
            json.dump(r.json(), f, indent=4)
        return r.json()
    

    def filter_anime(self, title_from_anilist:list[str], data, cutoff:int):
        anime_names = set()
        for anime in data:
            english_name = anime['title_english'].lower() if anime['title_english'] else 'a'
            title_name = anime['title'].lower() if anime['title'] else 'a'
            romanji_name = anime['title_romanji'].lower() if anime['title_romanji'] else 'a'

            for name in title_from_anilist:
                anime_name0 = difflib.get_close_matches(name, [english_name], n=1, cutoff=cutoff)
                anime_name1 = difflib.get_close_matches(name, [title_name], n=1, cutoff=cutoff)
                anime_name2 = difflib.get_close_matches(name, [romanji_name], n=1, cutoff=cutoff)

                if anime_name0 : anime_names.add(anime_name0[0])
                if anime_name1 : anime_names.add(anime_name1[0])
                if anime_name2 : anime_names.add(anime_name2[0])

        # For debug
        ic("First filtre:", anime_names, cutoff)

        anime_names2 = set()
        for name in title_from_anilist:
            anime_name = difflib.get_close_matches(name, anime_names, n=1, cutoff=cutoff)

            if anime_name : anime_names2.add(anime_name[0])

        if len(anime_names2) == 0 : return None

        # For debug
        ic("Second filtre:", anime_names2, cutoff)

        if len(anime_names2) > 1 and cutoff+0.05 < 1:
            return self.filter_anime(title_from_anilist, data, cutoff+0.05)
        else:
            return anime_names2.pop()


    def find_anime_in_neko_sama(self, title_from_anilist:list[str]):
        """Return the anime from neko_sama.json that is the closest to the title from anilist"""
        data = self.get_json()
        
        title_from_anilist = [title.lower() for title in title_from_anilist if title is not None]
        ic(title_from_anilist)

        anime_names = self.filter_anime(title_from_anilist, data, 0.89)
        ic(anime_names)

        # Get the anime from the json file
        for anime in data:
            english_name = anime['title_english'].lower() if anime['title_english'] else 'a'
            title_name = anime['title'].lower() if anime['title'] else 'a'
            romanji_name = anime['title_romanji'].lower() if anime['title_romanji'] else 'a'

            if anime_names in [english_name, title_name, romanji_name]:
                return anime
        return None



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

    def get_video_url_of(self, anime:dict, episode:int, lang:str):
        """Return the url of the episode from neko_sama.json"""

        url_episode = self.get_link_ep_anime(anime, episode, lang)
        ic(url_episode)
        r = requests.get(url_episode, verify=False)
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

    def get_link_ep_anime(self, anime:dict, episode:int, lang:str):
        """Return all the episodes from neko_sama.json"""
        
        # Build url episode
        tmp_url = anime['url'].split('/')[-1].split('-')
        end_url = tmp_url[-1].split('_')
        end_url.insert(1,f'-{str(abs(episode)).zfill(2)}_')
        tmp_url[-1] = ''.join(end_url)
        url = '-'.join(tmp_url)

        if lang == 'vf':
            url = url.replace('vostfr', 'vf')

        return "https://185.146.232.127/anime/episode/" + url

        # return "https://www.neko-sama.fr/anime/episode/" + url