from django.core.management.base import BaseCommand
from imdb_project.utils import get_movies_directed_by_director
from imdb_project.models import Director
class Command(BaseCommand):
    help = 'Get the number of movies directed by the director'

    def add_arguments(self, parser):
        parser.add_argument('director_name', type=str, help='Name of the director')

    def handle(self, *args, **options):
        try:
            director_name = options['director_name']
            director_obj=Director.objects.get(name=director_name)
            movies_count = get_movies_directed_by_director(director_obj=director_obj)
            if movies_count == 0:
                self.stdout.write(self.style.ERROR(f'Director with name {director_name} does not exist or has directed no movies.'))
            else:
                self.stdout.write(f'The director with name {director_name} has directed {movies_count} movies.')
        except Exception as e:
            print(f"Exception: {e}")
