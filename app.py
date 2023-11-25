import urllib3
import requests

from flask import Flask, render_template, request, jsonify

from anilist.anilist_api import get_ids_by_name, retrive_anime, top_anime_by_trends, top_anime_by_popularity, top_anime_this_season, get_current_season, get_recommendations_sorted_by_rating, get_random_anime
from anime.anime import create_anime_object

from scraping.neko_sama_scraping import NekoSamaScraper
from icecream import ic

app = Flask(__name__)
urllib3.disable_warnings()
requests.packages.urllib3.util.connection.HAS_IPV6 = False

@app.route('/')
def redirect():
    
    return index()

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

@app.route('/anime/<id>/<ep>/<lang>')
def anime(id:str, ep:str, lang:str):
    anime_data = retrive_anime(id)
    recommended_animes = [create_anime_object(anime['mediaRecommendation']) 
                          for anime in get_recommendations_sorted_by_rating(id)['data']['Media']['recommendations']['nodes'][:5]
                          ]

    anime = create_anime_object(anime_data['data']['Media'])

    anime_name_list = [anime.title['english'], anime.title['romaji']]

    neko_sama_scrapper = NekoSamaScraper("https://www.neko-sama.fr")

    anime_data_neko = neko_sama_scrapper.find_anime_in_neko_sama(anime_name_list)

    if anime_data_neko is None:
        return render_template('anime.html', id=id, ep=-1, lang=lang, anime=anime)

    urls_video = neko_sama_scrapper.get_video_url_of(anime_data_neko, int(ep), lang)
    if urls_video is None:
        return render_template('anime.html', id=id, ep=-1, lang=lang, anime=anime)

    nb_episodes = neko_sama_scrapper.get_nb_episodes(anime_data_neko, id)

    return render_template('anime.html', id=id, ep=int(ep), lang=lang, anime=anime, urls_video=urls_video, nb_episodes=nb_episodes, recommendations=recommended_animes)


@app.route('/top_anime')
def top_anime():
    trending_now = [create_anime_object(anime) for anime in top_anime_by_trends()]
    most_popular = [create_anime_object(anime) for anime in top_anime_by_popularity()]
    this_season = [create_anime_object(anime) for anime in top_anime_this_season()]

    current_season = get_current_season()

    return render_template('top_anime.html', trending_now=trending_now, most_popular=most_popular, 
                            this_season=this_season, current_season=current_season)

#background process happening without any refreshing
@app.route('/api/random_anime')
def random_anime():
    id = get_random_anime()
    ic(id)
    return {'id': id}, 200

@app.route('/api/delete-anime/', methods=['DELETE'])
def delete_anime():
    return jsonify(success=True), 204


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port="8081")