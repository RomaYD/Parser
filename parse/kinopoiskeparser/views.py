from django.shortcuts import render, get_object_or_404
import requests
import json
import time
from .models import Movie


class ParserOfKinopoisk:

    def parse(self):
        url = 'https://api.kinopoisk.dev/v1.4/movie?page=1&selectFields=id&selectFields=name&selectFields=description&selectFields=shortDescription&selectFields=type&selectFields=year&selectFields=movieLength&selectFields=ageRating&selectFields=genres&selectFields=persons&selectFields=watchability&type=movie&year=2020&genres.name=%D1%82%D1%80%D0%B8%D0%BB%D0%BB%D0%B5%D1%80'
        token = 'R937RPC-0354X76-NN8T6HQ-QCKPDAG' #токен как и ссылку необходимо убрать в скрытые данные, но сейчас для удобства ознакомления оставлю здесь
        session = requests.Session()
        session.headers.update({'X-API-KEY': token})
        response = session.get(url)
        json_of_movie = json.loads(response.text)
        pages = range(300, json_of_movie['pages'] + 1)
        for page in pages:
            url = 'https://api.kinopoisk.dev/v1.4/movie?page=' + str(
                page) + '&selectFields=id&selectFields=name&selectFields=description&selectFields=shortDescription&selectFields=type&selectFields=year&selectFields=movieLength&selectFields=ageRating&selectFields=genres&selectFields=persons&selectFields=watchability&selectFields=rating&type=movie&year=2020&genres.name=%D1%82%D1%80%D0%B8%D0%BB%D0%BB%D0%B5%D1%80'
            response = session.get(url)
            json_of_movies = json.loads(response.text)
            for movie in json_of_movies['docs']:
                id = movie['id']
                title = movie['name']
                type = movie['type']
                year = movie['year']  # int
                description = movie['description']
                short_description = movie['shortDescription']
                rating = ', '.join([key + ': ' + str(movie['rating'][key]) for key in movie['rating']])
                leanght = str(movie['movieLength']) + 'min'
                age_rating = movie['ageRating']  # int
                genres = ', '.join([movie['genres'][_]['name'] for _ in range(len(movie['genres']))])
                actors = []
                composers = []
                designers = []
                directors = []
                editors = []
                operators = []
                producers = []
                writers = []
                voice_actors = []
                for person in movie['persons']:
                    if person['enProfession'] == 'actor':
                        if person['name']:
                            actors.append(person['name'])
                        else:
                            actors.append(person['enName'])
                    elif person['enProfession'] == 'composer':
                        if person['name']:
                            composers.append(person['name'])
                        else:
                            composers.append(person['enName'])
                    elif person['enProfession'] == 'designer':
                        if person['name']:
                            designers.append(person['name'])
                        else:
                            designers.append(person['enName'])
                    elif person['enProfession'] == 'director':
                        if person['name']:
                            directors.append(person['name'])
                        else:
                            directors.append(person['enName'])
                    elif person['enProfession'] == 'editor':
                        if person['name']:
                            editors.append(person['name'])
                        else:
                            editors.append(person['enName'])
                    elif person['enProfession'] == 'editor':
                        if person['name']:
                            editors.append(person['name'])
                        else:
                            editors.append(person['enName'])
                    elif person['enProfession'] == 'operator':
                        if person['name']:
                            operators.append(person['name'])
                        else:
                            operators.append(person['enName'])
                    elif person['enProfession'] == 'producer':
                        if person['name']:
                            producers.append(person['name'])
                        else:
                            producers.append(person['enName'])
                    elif person['enProfession'] == 'writer':
                        if person['name']:
                            writers.append(person['name'])
                        else:
                            writers.append(person['enName'])
                    elif person['enProfession'] == 'voice_actor':
                        if person['name']:
                            voice_actors.append(person['name'])
                        else:
                            voice_actors.append(person['enName'])
                    actors_str = ', '.join(actors)
                    composers_str = ', '.join(composers)
                    designers_str = ', '.join(designers)
                    directors_str = ', '.join(directors)
                    editors_str = ', '.join(editors)
                    operators_str = ', '.join(operators)
                    producers_str = ', '.join(producers)
                    writers_str = ', '.join(writers)
                    voice_actors_str = ', '.join(voice_actors)
                    movie_obj = Movie(
                        id=id,
                        title=title,
                        type=type,
                        year=year,
                        description=description,
                        rating=rating,
                        short_description=short_description,
                        leanght=leanght,
                        age_rating=age_rating,
                        genres=genres,
                        actors=actors_str,
                        composers=composers_str,
                        designers=designers_str,
                        directors=directors_str,
                        editors=editors_str,
                        operators=operators_str,
                        producers=producers_str,
                        writers=writers_str,
                        voice_actors=voice_actors_str,
                    )
                    movie_obj.save()


def start_parse(request):
    parser = ParserOfKinopoisk()
    parser.parse()
    films = Movie.objects.all()
    context = {'films': films}
    return render(request, 'parser_res.html', context)


def render_detail_inf(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    actors = movie.actors.split(', ')
    composers = movie.composers.split(', ')
    designers = movie.designers.split(', ')
    directors = movie.directors.split(', ')
    editors = movie.editors.split(', ')
    operators = movie.operators.split(', ')
    producers = movie.producers.split(', ')
    writers = movie.writers.split(', ')
    voice_actors = movie.voice_actors.split(', ')
    context = {'movie': movie,
               'actors': actors,
               'composers': composers,
               'editors': editors,
               'designers': designers,
               'directors': directors,
               'operators': operators,
               'producers': producers,
               'writers': writers,
               'voice_actors': voice_actors}

    return render(request, 'film_detail.html', context)
