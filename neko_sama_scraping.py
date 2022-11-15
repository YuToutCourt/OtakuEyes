import logging
import os, re
import json
import difflib
import random
import requests

from bs4 import BeautifulSoup

URL = "https://neko-sama.fr/animes-search-vostfr.json"

def get_json():
    """Return the json file from neko_sama.json"""

    # Get the json file
    if os.path.exists('neko_sama.json') and random.randint(0, 10) < 4:
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

    try:
        # Get the anime title from neko_sama.json that is the closest to the title from anilist
        anime_name = difflib.get_close_matches(title_from_anilist, [anime['title_english'] for anime in data], n=1, cutoff=0.6)
    
    except Exception as e:
        logging.error(e)
        return None
    
    print(f"-----DEBUG :\nAnilist: {title_from_anilist}\nNeko Sama: {anime_name}\n-----")

    # If there is no anime that is close enough
    if len(anime_name) == 0: return None

    # Get the anime from neko_sama.json
    for anime in data:
        if anime['title_english'] == anime_name[0]:
            return anime

def get_nb_episodes(anime:dict):
    """Return the number of episodes from neko_sama.json"""
    if anime['type'] == "m0v1e":
        return 1

    value = anime['nb_eps'].split(' ')[0]
    if value.isdigit():
        return int(value)
    
    # If the number of episodes is unknown (ex: ?) use a default value of 100 episodes (it's enough)
    return 100

def get_video_url_of(anime:dict, episode:int):
    """Return the url of the episode from neko_sama.json"""

    url_episode = get_link_ep_anime(anime, episode)

    r = requests.get(url_episode)
    soup = BeautifulSoup(r.text, 'lxml')

    # Don't ask me I have done black magic
    script = soup.find_all('script')
    script = script[2].text

    index_= script.index('else')
    str_ = script[index_:index_+100]

    # find the url in the string
    url = re.findall(r'(https?://[^\s]+)', str_)[0]
    url = url.split("'")[0]

    return url

def get_link_ep_anime(anime:dict, episode:int):
    """Return all the episodes from neko_sama.json"""

    # Build url episode
    tmp_url = anime['url'].split('/')[-1].split('-')
    tmp_url.insert(-1, str(episode).zfill(2))
    url = '-'.join(tmp_url)

    return "https://www.neko-sama.fr/anime/episode/" + url
