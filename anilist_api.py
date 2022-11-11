import requests


URL = 'https://graphql.anilist.co'

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