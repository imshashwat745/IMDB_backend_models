from django.core.management.base import BaseCommand
from imdb_project.utils import get_average_rating_of_movie
from imdb_project.models import Movie
class Command(BaseCommand):
    help = 'Get the average rating of a movie'

    def add_arguments(self, parser):
        parser.add_argument('movie_id', type=str, help='Name of the movie')

    def handle(self, *args, **options):
        try:
            movie_id = options['movie_id']
            movie_obj=Movie.objects.get(movie_id=movie_id)
            average_rating = get_average_rating_of_movie(movie_obj=movie_obj)
            if average_rating == 0:
                self.stdout.write(self.style.ERROR(f'Rating for movie with ID {movie_id} does not exist.'))
            else:
                self.stdout.write(f'The movie with ID {movie_id} has average rating of {average_rating}')
        except Exception as e:
            print(f"Exception: {e}")
