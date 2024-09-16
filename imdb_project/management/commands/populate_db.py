# imdb_project/management/commands/populate_db.py

from django.core.management.base import BaseCommand
from imdb_project.utils import populate_database

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        actors_list = [
            {"actor_id": "actor_1", "name": "Actor 1"},
            {"actor_id": "actor_2", "name": "Actor 2john"}
        ]

        movies_list = [
            {
                "movie_id": "movie_1",
                "name": "Movie 1",
                "actors": [
                    {"actor_id": "actor_1", "role": "hero", "is_debut_movie": False},
                    {"actor_id": "actor_2", "role": "sidekick", "is_debut_movie": True}
                ],
                "box_office_collection_in_crores": "15.6",
                "release_date": "2022-05-15",
                "director_name": "Director 1"
            },
            {
                "movie_id": "movie_2",
                "name": "Movie 2",
                "actors": [
                    {"actor_id": "actor_1", "role": "villain", "is_debut_movie": False}
                ],
                "box_office_collection_in_crores": "7.8",
                "release_date": "2023-08-21",
                "director_name": "Director 2"
            }
        ]

        directors_list = ["Director 1", "Director 2"]

        movie_rating_list = [
            {
                "movie_id": "movie_1",
                "rating_one_count": 2,
                "rating_two_count": 3,
                "rating_three_count": 7,
                "rating_four_count": 5,
                "rating_five_count": 10
            },
            {
                "movie_id": "movie_2",
                "rating_one_count": 1,
                "rating_two_count": 2,
                "rating_three_count": 5,
                "rating_four_count": 3,
                "rating_five_count": 6
            }
        ]

        populate_database(actors_list, movies_list, directors_list, movie_rating_list)
        self.stdout.write(self.style.SUCCESS('Database populated successfully'))
