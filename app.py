from flask import Flask, render_template, request

from anilist_api import get_ids_by_name, retrive_anime
from anime import create_anime_object

from neko_sama_scraping import find_anime_in_neko_sama, get_all_episodes_from_neko_sama

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/browse', methods=['POST'])
def browse():
    name = request.form['search']
    anime_data = get_ids_by_name(name)
    animes = [create_anime_object(anime) for anime in anime_data['data']['Page']['media'] if anime['format'] not in ["MANGA", "NOVEL", "ONE_SHOT", "MUSIC", "LIGHT_NOVEL", "VISUAL_NOVEL"]]
    return render_template('browse.html', animes=animes)


@app.route('/anime/<id>')
def anime(id):
    anime_data = retrive_anime(id)
    anime = create_anime_object(anime_data['data']['Media'])

    list_episodes = get_all_episodes_from_neko_sama(find_anime_in_neko_sama(anime.title['romaji']))

    return render_template('anime.html', id=id, anime=anime, list_episodes=list_episodes)

if __name__ == '__main__':
    app.run(debug=True)