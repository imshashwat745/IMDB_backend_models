from typing import List

from django.core.management.base import BaseCommand
from pyparsing import empty

from imdb_project.utils import get_all_actor_objects_acted_in_given_movies
from imdb_project.models import Movie
class Command(BaseCommand):
    help = 'Get all actor objects acted in given movies'

    def add_arguments(self, parser):
        # parser.add_argument('movies', type=List[str], help='Name of the actor')
        parser.add_argument(
            'movies',
            nargs='+',  # This allows multiple arguments
            type=str,
            help='List of movie IDs'
        )

    def handle(self, *args, **options):
        try:
            movies = options['movies']
            movies_obj=[]
            for movie in movies:
                movies_obj.append(Movie.objects.get(movie_id=movie))
            print(movies_obj)
            actors= get_all_actor_objects_acted_in_given_movies(movie_objs=movies_obj)
            if len(actors) == 0:
                self.stdout.write(self.style.ERROR(f'No actors found'))
            else:
                self.stdout.write(f'The actors object is: {actors}')
        except Exception as e:
            print(f"Exception: {e}")
