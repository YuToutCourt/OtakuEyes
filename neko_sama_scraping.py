import os, re
import json
import difflib
import requests

from bs4 import BeautifulSoup

URL = "https://neko-sama.fr/animes-search-vostfr.json"

def get_json():
    """Return the json file from neko_sama.json"""

    if os.path.exists('neko_sama.json'):
        with open('neko_sama.json', 'r') as f:
            return json.load(f)
    else:
        r = requests.get(URL)
        with open('neko_sama.json', 'w') as f:
            json.dump(r.json(), f)
        return r.json()


def find_anime_in_neko_sama(title_from_anilist:str):
    """Return the anime from neko_sama.json that is the closest to the title from anilist"""
    data = get_json()

    anime_name = difflib.get_close_matches(title_from_anilist, [anime['title'] for anime in data], n=1, cutoff=0.6)

    for anime in data:
        if anime['title'] == anime_name[0]:
            return anime
    
    return None


def get_all_episodes_from_neko_sama(anime:dict):
    """Return all the episodes from neko_sama.json"""

    # Build url episode
    nb_episode = int(anime['nb_eps'].split(' ')[0])
    tmp_url = anime['url'].split('/')[-1].split('-')
    tmp_url.insert(-1, "01")
    url = '-'.join(tmp_url)

    # Get all links of the episodes to parse
    episodes = []
    for i in range(1, nb_episode + 1):
        episodes.append(url.replace('01', str(i).zfill(2)))
    
    # Parse all the episodes
    all_episodes = []
    for episode in episodes:
        r = requests.get(f"https://www.neko-sama.fr/anime/episode/{episode}")
        soup = BeautifulSoup(r.text, 'lxml')

        # Don't ask me I have done black magic
        script = soup.find_all('script')
        print(script)
        script = script[2].text

        index_= script.index('else')
        str_ = script[index_:index_+100]

        # find the url in the string
        url = re.findall(r'(https?://[^\s]+)', str_)[0]
        url = url.split("'")[0]

        all_episodes.append(url)

    return all_episodes