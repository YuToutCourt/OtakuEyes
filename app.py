from flask import Flask, render_template, request

from anilist_api import get_ids_by_name, retrive_anime
from anime import create_anime_object

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/browse', methods=['POST'])
def browse():
    name = request.form['search']
    anime_data = get_ids_by_name(name)
    animes = [create_anime_object(anime) for anime in anime_data['data']['Page']['media']]
    return render_template('browse.html', animes=animes)


@app.route('/anime/<id>')
def anime(id):
    anime_data = retrive_anime(id)
    anime = create_anime_object(anime_data['data']['Media'])
    return render_template('anime.html', id=id, anime=anime)

if __name__ == '__main__':
    app.run(debug=True)