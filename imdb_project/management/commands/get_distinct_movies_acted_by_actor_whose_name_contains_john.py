from django.core.management.base import BaseCommand
from imdb_project.utils import get_distinct_movies_acted_by_actor_whose_name_contains_john
from imdb_project.models import Movie, Director


class Command(BaseCommand):
    help = 'get_distinct_movies_acted_by_actor_whose_name_contains_john'


    def add_arguments(self, parser):
        pass
    def handle(self, *args, **options):
        try:
            movies=get_distinct_movies_acted_by_actor_whose_name_contains_john()
            if len(movies) == 0:
                self.stdout.write(self.style.ERROR(f'No movies found'))
            else:
                self.stdout.write(f'Movies are: {movies}')
        except Exception as e:
            print(f"Exception: {e}")
