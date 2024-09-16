from django.core.management.base import BaseCommand
from imdb_project.utils import delete_movie_rating
from imdb_project.models import Movie
class Command(BaseCommand):
    help = 'Delete rating object of a movie'

    def add_arguments(self, parser):
        parser.add_argument('movie_id', type=str, help='Name of the movie')

    def handle(self, *args, **options):
        try:
            movie_id = options['movie_id']
            movie_obj=Movie.objects.get(movie_id=movie_id)
            delete_result= delete_movie_rating(movie_obj=movie_obj)
            if delete_result != 1:
                self.stdout.write(self.style.ERROR(f'Rating of movie with ID {movie_id} could not be deleted due to Exception: {delete_result}'))
            else:
                self.stdout.write(f'Rating object of movie with ID {movie_id} deleted successfully')
        except Exception as e:
            print(f"Exception: {e}")
