from django.core.management.base import BaseCommand
from imdb_project.utils import update_director_for_given_movie
from imdb_project.models import Movie, Director


class Command(BaseCommand):
    help = 'Update director of a given movie'

    def add_arguments(self, parser):
        parser.add_argument('movie_id', type=str, help='Name of the movie')
        parser.add_argument('director_name', type=str, help='Name of the director')

    def handle(self, *args, **options):
        try:
            movie_id = options['movie_id']
            director_name=options["director_name"]
            movie_obj=Movie.objects.get(movie_id=movie_id)
            director_obj=Director.objects.get(name=director_name)
            update_result= update_director_for_given_movie(movie_obj=movie_obj, director_obj=director_obj)
            if update_result != 1:
                self.stdout.write(self.style.ERROR(f'Director of movie with ID {movie_id} could not be updated due to Exception: {update_result}'))
            else:
                self.stdout.write(f'Director object of movie with ID {movie_id} updated successfully')
        except Exception as e:
            print(f"Exception: {e}")
