from django.core.management.base import BaseCommand
from imdb_project.utils import get_all_rating_objects_for_given_movies
from imdb_project.models import Movie, Director


class Command(BaseCommand):
    help = 'Get rating objects for given movies'

    def add_arguments(self, parser):
        parser.add_argument(
            'movies',
            nargs='+',  # This allows multiple arguments
            type=str,
            help='List of movie IDs'
        )

    def handle(self, *args, **options):
        try:
            movies = options['movies']
            movies_obj = []
            for movie in movies:
                movies_obj.append(Movie.objects.get(movie_id=movie))
            print(movies_obj)
            ratings = get_all_rating_objects_for_given_movies(movie_objs=movies_obj)
            if len(ratings) == 0:
                self.stdout.write(self.style.ERROR(f'No ratings found'))
            else:
                self.stdout.write(f'The actors object is: {ratings}')
        except Exception as e:
            print(f"Exception: {e}")


