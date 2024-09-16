from django.core.management.base import BaseCommand
from imdb_project.utils import remove_all_actors_from_given_movie
from imdb_project.models import Movie, Director


class Command(BaseCommand):
    help = 'Remove all actors from a given movie'

    def add_arguments(self, parser):
        parser.add_argument('movie_id', type=str, help='Name of the movie')

    def handle(self, *args, **options):
        try:
            movie_id = options['movie_id']
            movie_obj=Movie.objects.get(movie_id=movie_id)
            deletion_result= remove_all_actors_from_given_movie(movie_obj=movie_obj)
            if deletion_result != 1:
                self.stdout.write(self.style.ERROR(f'Deletion failed due to Exception: {deletion_result}'))
            else:
                self.stdout.write(f'Deleted successfully')
        except Exception as e:
            print(f"Exception: {e}")
