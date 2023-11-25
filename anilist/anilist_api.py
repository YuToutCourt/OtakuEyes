import random
import requests

from datetime import datetime
from icecream import ic

SEASON = ['WINTER', 'SPRING', 'SUMMER', 'FALL']
URL = 'https://graphql.anilist.co'

def get_random_anime():
    from scraping.neko_sama_scraping import NekoSamaScraper
    neko_sama = NekoSamaScraper("https://185.146.232.127")

    query = '''
    query ($type: MediaType, $isAdult: Boolean, $perPage: Int, $page: Int) {
      Page (perPage: $perPage, page: $page) {
        pageInfo {
          perPage
        }
        media (type: $type, isAdult: $isAdult) {
          id
          popularity
          title {
            romaji
            english
            native
          }
        }
      }
    }
    '''

    variables = {
        'type': 'ANIME',
        'isAdult': False,
        'perPage': 50, # 50 is the max
        'page': random.randint(1, 344)# 344 is the last page
    }

    response = requests.post(URL, json={'query': query, 'variables': variables})
    data = response.json()
    anime_list = data['data']['Page']['media']

    random_anime = random.choice(anime_list)
    ic(random_anime)

    title = [random_anime['title']['romaji'], random_anime['title']['english'], random_anime['title']['native']]

    if neko_sama.find_anime_in_neko_sama(title) is None:
        return get_random_anime()

    popularity = random_anime['popularity']
    if popularity < 1000:
        return get_random_anime()

    return random_anime['id']

def get_current_season():
    return SEASON[(datetime.now().month -1) // 3]

def top_anime_by_trends(page=1, per_page=6, sort=['TRENDING_DESC']):
    query = '''
    query ($page: Int, $perPage: Int, $sort: [MediaSort]) {
        Page (page: $page, perPage: $perPage) {
            pageInfo {
                total
                currentPage
                lastPage
                hasNextPage
                perPage
            }
            media (sort: $sort, type: ANIME) {
                id
                title {
                  romaji
                  english
                  native      
                }
                coverImage {
                  large
                  color                  
                }
                genres
                status
                description
                bannerImage
                isAdult
                format
            }
        }
    }
    '''
    variables = {
        'page': page,
        'perPage': per_page,
        'sort': sort
    }

    response = requests.post(URL, json={'query': query, 'variables': variables})

    return response.json().get('data').get('Page').get('media')

def top_anime_by_popularity(page=1, per_page=6, sort=['POPULARITY_DESC']):
    query = '''
    query ($page: Int, $perPage: Int, $sort: [MediaSort]) {
        Page (page: $page, perPage: $perPage) {
            pageInfo {
                total
                currentPage
                lastPage
                hasNextPage
                perPage
            }
            media (sort: $sort, type: ANIME) {
                id
                title {
                  romaji
                  english
                  native      
                }
                coverImage {
                  large
                  color                  
                }
                genres
                status
                description
                bannerImage
                isAdult
                format
            }
        }
    }
    '''
    variables = {
        'page': page,
        'perPage': per_page,
        'sort': sort
    }

    response = requests.post(URL, json={'query': query, 'variables': variables})

    return response.json().get('data').get('Page').get('media')
  
def top_anime_this_season(page=1, per_page=6, sort=['POPULARITY_DESC']):
    season = get_current_season()
    season_year = datetime.now().year
    query = '''
    query ($page: Int, $perPage: Int, $sort: [MediaSort], $season: MediaSeason, $seasonYear: Int) {
        Page (page: $page, perPage: $perPage) {
            pageInfo {
                total
                currentPage
                lastPage
                hasNextPage
                perPage
            }
            media (sort: $sort, type: ANIME, season: $season, seasonYear: $seasonYear) {
                id
                title {
                  romaji
                  english
                  native      
                }
                coverImage {
                  large
                  color                  
                }
                genres
                status
                description
                bannerImage
                isAdult
                format
            }
        }
    }
    '''
    variables = {
        'page': page,
        'perPage': per_page,
        'sort': sort,
        'season': season,
        'seasonYear': season_year
    }

    response = requests.post(URL, json={'query': query, 'variables': variables})

    return response.json().get('data').get('Page').get('media')

def get_id_by_name(anime_name):
    query = f'''
    query ($search: String) {{
      Media (search: $search, type: ANIME) {{
        id
      }}
    }}
    '''

    variables = { 'search': anime_name }

    response = requests.post(URL, json={'query': query, 'variables': variables})

    return response.json()

def get_ids_by_name(anime_name):
    query = '''
    query ($id: Int, $page: Int, $perPage: Int, $search: String) {
        Page (page: $page, perPage: $perPage) {
            pageInfo {
                total
                currentPage
                lastPage
                hasNextPage
                perPage
            }
            media (id: $id, search: $search, type: ANIME) {
                id
                title {
                  romaji
                  english
                  native      
                }
                coverImage {
                  large
                  color                  
                }
                genres
                status
                description
                bannerImage
                isAdult
                format
            }
        }
    }
    '''
    variables = {
        'search': anime_name,
        'page': 1,
        'perPage': 100
    }

    response = requests.post(URL, json={'query': query, 'variables': variables})

    return response.json()

def retrive_anime(id):
    query = f'''
    query ($id: Int) {{
      Media (id: $id, type: ANIME) {{
        id
        title {{
          romaji
          english
          native
        }}
        coverImage {{
          large
          color
        }}
          genres
          status
          description
          bannerImage
          isAdult                    
      }}
    }}
    '''

    variables = { 'id': id }

    response = requests.post(URL, json={'query': query, 'variables': variables})

    return response.json()

def get_next_ep(id):
    query = '''
    query ($id: Int) {
        Media (id: $id, type: ANIME) {
            nextAiringEpisode {
                episode
            }
        }
    }
    '''

    variables = { 'id': id }

    response = requests.post(URL, json={'query': query, 'variables': variables})

    return response.json()

def get_recommendations_sorted_by_rating(id):
    query = '''
        query ($id: Int!) {
            Media (id: $id) {
                recommendations (sort: RATING_DESC) {
                    nodes {
                        rating
                        mediaRecommendation {
                            id
                            title {
                              romaji
                              english
                              native
                            }
                            coverImage {
                                large
                                color
                            }
                              genres
                              status
                              description
                              bannerImage
                              isAdult    
                        }
                    }
                }
            }
        }
    '''

    variables = { 'id': id }

    response = requests.post(URL, json={'query': query, 'variables': variables})

    return response.json()
