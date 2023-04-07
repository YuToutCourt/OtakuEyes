import urllib3

from flask import Flask, render_template, request

from anilist.anilist_api import get_ids_by_name, retrive_anime, top_anime_by_trends, top_anime_by_popularity, top_anime_this_season, get_current_season
from anime.anime import create_anime_object

from scraping.neko_sama_scraping import NekoSamaScraper

app = Flask(__name__)
urllib3.disable_warnings()

@app.route('/')
def redirect():
    neko_sama = NekoSamaScraper("https://185.146.232.127")

    anime_main_page = neko_sama.scrap_main_page()
    
    return render_template('index.html', anime_main_page=anime_main_page)

@app.route('/home')
def index():
    neko_sama = NekoSamaScraper("https://185.146.232.127")


    anime_main_page = neko_sama.scrap_main_page()
    
    return render_template('index.html', anime_main_page=anime_main_page)

@app.route('/browse', methods=['POST'])
def browse():
    name = request.form['search']
    anime_data = get_ids_by_name(name)

    animes = [create_anime_object(anime) for anime in anime_data['data']['Page']['media'] 
                if anime['format'] not in ["MANGA", "NOVEL", "ONE_SHOT", "MUSIC", "LIGHT_NOVEL", "VISUAL_NOVEL", "SPECIAL"] and \
                    anime['status'] not in ["NOT_YET_RELEASED", "CANCELLED"] and anime['isAdult'] == False]

    return render_template('browse.html', animes=animes)

@app.route('/anime/<id>/<ep>')
def anime(id, ep):
    anime_data = retrive_anime(id)

    anime = create_anime_object(anime_data['data']['Media'])

    anime_name_list = [anime.title['english'], anime.title['romaji']]

    neko_sama_scrapper = NekoSamaScraper("https://www.neko-sama.fr")
    print(neko_sama_scrapper.url)

    anime_data_neko = neko_sama_scrapper.find_anime_in_neko_sama(anime_name_list)
    print(anime_data_neko)
    if anime_data_neko is None:
        return render_template('anime.html', id=id, ep=-1, anime=anime)

    urls_video = neko_sama_scrapper.get_video_url_of(anime_data_neko, ep)
    if urls_video is None:
        return render_template('anime.html', id=id, ep=-1, anime=anime)

    nb_episodes = neko_sama_scrapper.get_nb_episodes(anime_data_neko, id)

    return render_template('anime.html', id=id, ep=int(ep), anime=anime, urls_video=urls_video, nb_episodes=nb_episodes)


@app.route('/top_anime')
def top_anime():
    trending_now = [create_anime_object(anime) for anime in top_anime_by_trends()]
    most_popular = [create_anime_object(anime) for anime in top_anime_by_popularity()]
    this_season = [create_anime_object(anime) for anime in top_anime_this_season()]

    current_season = get_current_season()

    return render_template('top_anime.html', trending_now=trending_now, most_popular=most_popular, 
                            this_season=this_season, current_season=current_season)

if __name__ == '__main__':
    app.run(debug=True)