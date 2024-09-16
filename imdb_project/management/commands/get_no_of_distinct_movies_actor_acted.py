from django.core.management.base import BaseCommand
from imdb_project.utils import get_no_of_distinct_movies_actor_acted

class Command(BaseCommand):
    help = 'Get the number of distinct movies an actor has acted in'

    def add_arguments(self, parser):
        parser.add_argument('actor_id', type=str, help='ID of the actor')

    def handle(self, *args, **options):
        self.stdout.write("1")

        actor_id = options['actor_id']
        self.stdout.write(actor_id)
        distinct_movies_count = get_no_of_distinct_movies_actor_acted(actor_id)

        if distinct_movies_count == 0:
            self.stdout.write(self.style.ERROR(f'Actor with ID {actor_id} does not exist or has no movies.'))
        else:
            self.stdout.write(f'The actor with ID {actor_id} has acted in {distinct_movies_count} distinct movies.')
