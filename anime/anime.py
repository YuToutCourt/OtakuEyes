import re
from typing import List

class Anime:
    def __init__(self, id:int, title:dict[str], image_url:str, description:str, 
                    genres:List[str], color:str, status:str, is_adult:bool, 
                    banner_image:str, format:str, episode:int=None):
        self.id = id
        self.title = title
        self.image_url = image_url
        self.description = re.sub('<[^<]+?>', '', description) if description else None
        self.genres = genres
        self.color = color
        self.status = status
        self.is_adult = is_adult
        self.banner_image = banner_image
        self.format = format
        self.episode = episode


    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other) -> bool:
        return self.id == other.id


def create_anime_object(anime_data: dict) :
    """
    :param anime_data: The data returned by the Anilist API

    Creates an Anime object from the data returned by the Anilist API

    :return: Anime object
    """
    id = anime_data.get('id')
    title = anime_data.get('title')
    image_url = anime_data.get('coverImage').get('large')
    description = anime_data.get('description')
    genres = anime_data.get('genres')
    color = anime_data.get('coverImage').get('color')
    status = anime_data.get('status')
    is_adult = anime_data.get('isAdult')
    banner_image = anime_data.get('bannerImage')
    format = anime_data.get('format')

    if anime_data.get('episodes') is not None:
        episodes = anime_data.get('episodes')
    else:
        episodes = None

    if len(genres) == 0: 
        genres = ['Unknown']

    return Anime(id, title, image_url, description, genres, color, status, is_adult, banner_image, format, episodes)