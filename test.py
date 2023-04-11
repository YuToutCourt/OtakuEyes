import difflib
import json

def trouver_nom_plus_proche(liste_noms):
    with open('neko_sama.json', 'r') as f:
        data = json.load(f)

    noms_anime = set()

    for name in liste_noms:

        anime_name0 = difflib.get_close_matches(name.lower(), [anime['title_english'].lower() if anime["title_english"] else 'a' for anime in data], n=1, cutoff=0.6)
        anime_name1 = difflib.get_close_matches(name.lower(), [anime['title'].lower() if anime['title'] else 'a' for anime in data], n=1, cutoff=0.6)
        anime_name2 = difflib.get_close_matches(name.lower(), [anime['title_romanji'].lower() if anime['title_romanji'] else 'a' for anime in data], n=1, cutoff=0.6)

        if anime_name0 : noms_anime.add(anime_name0[0])
        if anime_name1 : noms_anime.add(anime_name1[0])
        if anime_name2 : noms_anime.add(anime_name2[0])

    print(noms_anime)
    
    noms_anime_2 = set()
    for name in liste_noms:
        anime_name = difflib.get_close_matches(name.lower(), noms_anime, n=1, cutoff=0.6)

        if anime_name : noms_anime_2.add(anime_name[0])

    print(noms_anime_2)

    for anime in data:
        english_name = anime['title_english'].lower() if anime['title_english'] else 'a'
        title_name = anime['title'].lower() if anime['title'] else 'a'
        romanji_name = anime['title_romanji'].lower() if anime['title_romanji'] else 'a'
        for name in noms_anime_2:
            if name in english_name or name in title_name or name in romanji_name:
                return anime
    
    return None


l = ['Fullmetal Alchemist: Brotherhoo', 'Hagane no Renkinjutsushi: FULLMETAL ALCHEMIST']

print(trouver_nom_plus_proche(l))