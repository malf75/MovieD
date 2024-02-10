import json
from django.core.management.base import BaseCommand
from Movied.models import Filmes

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='The path to the JSON file')

    def handle(self, *args, **kwargs):
        json_file_path = kwargs['json_file']
        
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            for item in data['filmes']:
                released_year = item.get('Released_Year')
                if released_year and isinstance(released_year, int):
                    released_year_value = released_year
                else:
                    released_year_value = None

                new_filme = Filmes(
                    Poster_Link=item['Poster_Link'],
                    Series_Title=item['Series_Title'],
                    Released_Year=released_year_value,
                    Runtime=item['Runtime'],
                    Genre=item['Genre'],
                    Rating=item['IMDB_Rating'],
                    Overview=item['Overview'],
                )
                new_filme.save()