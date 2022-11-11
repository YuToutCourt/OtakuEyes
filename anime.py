import re

class Anime:
    def __init__(self, id, title, image_url, description, genres, color, status, is_adult, banner_image):
        self.id = id
        self.title = title
        self.image_url = image_url
        self.description = re.sub('<[^<]+?>', '', description) if description else None
        self.genres = genres
        self.color = color
        self.status = status
        self.is_adult = is_adult
        self.banner_image = banner_image


def create_anime_object(anime_data: dict) :
    id = anime_data.get('id')
    title = anime_data.get('title').get('romaji')
    image_url = anime_data.get('coverImage').get('large')
    description = anime_data.get('description')
    genres = anime_data.get('genres')[:2]
    color = anime_data.get('coverImage').get('color')
    status = anime_data.get('status')
    is_adult = anime_data.get('isAdult')
    banner_image = anime_data.get('bannerImage') 

    if len(genres) == 0: 
        genres = ['Unknown']

    return Anime(id, title, image_url, description, genres, color, status, is_adult, banner_image)