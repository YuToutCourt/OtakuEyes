import requests

from datetime import datetime


SEASON = ['WINTER', 'SPRING', 'SUMMER', 'FALL']
URL = 'https://graphql.anilist.co'

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
    season = SEASON[(datetime.now().month -1) // 3]
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