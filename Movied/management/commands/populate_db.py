import requests
import time
from django.core.management.base import BaseCommand
from Movied.models import Filmes

class Command(BaseCommand):
    help = 'Fetch and store movie data from the TMDb API into the database'

    def add_arguments(self, parser):
        parser.add_argument('api_key', type=str, help='The TMDb API key')

    def handle(self, *args, **kwargs):

        api_key = kwargs['api_key']
        base_url = 'https://api.themoviedb.org/3/movie/'

        def get_movie_data(movie_id):
            url = f"{base_url}{movie_id}?api_key={api_key}"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                # Exceeded rate limit
                self.stdout.write("Rate limit exceeded, waiting before retrying...")
                time.sleep(2)  # Espera 2 segundos antes de tentar novamente
                return get_movie_data(movie_id)
            else:
                return None

        for movie_id in range(1, 2001):
            self.stdout.write(f"Fetching data for movie ID: {movie_id}")
            movie_data = get_movie_data(movie_id)
            if movie_data:
                # Extrair os dados necessários
                released_year = movie_data.get('release_date', '').split('-')[0]
                if released_year.isdigit():
                    released_year_value = int(released_year)
                else:
                    released_year_value = None

                # Criar e salvar o novo objeto Filme
                new_filme = Filmes(
                    Poster_Link=f"https://image.tmdb.org/t/p/w500{movie_data.get('poster_path', '')}",
                    Series_Title=movie_data.get('title', ''),
                    Released_Year=released_year_value,
                    Runtime=movie_data.get('runtime', ''),
                    Genre=', '.join([genre['name'] for genre in movie_data.get('genres', [])]),
                    Rating=movie_data.get('vote_average', 0.0),
                    Overview=movie_data.get('overview', ''),
                )
                new_filme.save()

            # Pausa para respeitar o limite de requisições
            time.sleep(0.02)  # 50 requests per second = 1 request every 0.02 seconds

        self.stdout.write("Movie data has been successfully saved to the database")