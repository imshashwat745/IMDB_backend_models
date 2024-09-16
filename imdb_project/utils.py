from threading import activeCount
from typing import List, Dict
from unicodedata import category

from aptdaemon.lock import release

from .models import Actor, Cast, CastDetails, Director, Role, Rating, Movie

def populate_database(actors_list, movies_list, directors_list, movie_rating_list):
    """
        :param actors_list:[
            {
                "actor_id": "actor_1",
                "name": "Actor 1"
            }
        ]
        :param movies_list: [
            {
                "movie_id": "movie_1",
                "name": "Movie 1",
                "actors": [
                    {
                        "actor_id": "actor_1",
                        "role": "hero",
                        "is_debut_movie": False
                    }
                ],
                "box_office_collection_in_crores": "12.3",
                "release_date": "2020-3-3",
                "director_name": "Director 1"
            }
        ]
        :param directors_list: [
            "Director 1"
        ]
        :param movie_rating_list: [
            {
                "movie_id": "movie_1",
                "rating_one_count": 4,
                "rating_two_count": 4,
                "rating_three_count": 4,
                "rating_four_count": 4,
                "rating_five_count": 4
            }
        ]
    """

    # Create or Retrieve directors
    directors={}
    for directors_name in directors_list:
        director, created=Director.objects.get_or_create(name=directors_name)
        directors[directors_name]=director

    # Create or retrieve actors
    actors={}
    for actor in actors_list:
        actor_id=actor["actor_id"]
        actor_name=actor["name"]
        actor, created=Actor.objects.get_or_create(actor_id=actor_id, defaults={'name': actor_name})
        actors[actor_id]=actor

    # Create or retrieve roles
    roles={}
    for movie_data in movies_list:
        for actor_data in movie_data["actors"]:
            role_name=actor_data["role"]
            role, created=Role.objects.get_or_create(role_name=role_name)
            roles[role_name]=role

    # Create or retrieve movies
    for movie_data in movies_list:
        movie_id=movie_data["movie_id"]
        movie_name=movie_data["name"]
        release_date=movie_data["release_date"]
        box_office_collection_in_crores=float(movie_data["box_office_collection_in_crores"])
        director_name=movie_data["director_name"]

        # Get the director
        director=directors.get(director_name)
        if not director:
            raise ValueError(f"Director '{director_name}' not found")

        # Create cast object
        cast=Cast.objects.create()
        # if cast:
        #     print(cast.id)

        # Create movie object
        movie, created= Movie.objects.get_or_create(movie_id=movie_id,
                                                    defaults={
                                                        'name': movie_name,
                                                        'release_date': release_date,
                                                        'box_office_collection_in_crores': box_office_collection_in_crores,
                                                        'director': director,
                                                        'cast': cast
                                                    })

        # Update CastDetails

        actors_roles_dict :Dict[str,List[str]]={}
        debutants_list: List[str]=[]

        # Segregate all actors with their roles and debutants information
        for actor_element in movie_data["actors"]:
            role=actor_element["role"]
            actor_id=actor_element["actor_id"]
            is_debut_movie=actor_element["is_debut_movie"]
            if actor_id not in debutants_list and is_debut_movie:
                debutants_list.append(actor_id)
            if actor_id not in actors_roles_dict.keys():
                actors_roles_dict[actor_id]=[]
            actors_roles_dict[actor_id].append(role)

    #     Now update CastDetails
        for actor_id in actors_roles_dict.keys():
            actor=actors.get(actor_id)
            if not actor:
                raise ValueError(f"No actor with actor_id '{actor_id}'")
            roles_of_actor=actors_roles_dict.get(actor_id)
            role_objects=[roles[role_name] for role_name in roles_of_actor]
            is_debut_movie=actor_id in debutants_list
            cast_details, created= CastDetails.objects.get_or_create(
                cast=cast,
                actor=actor,
                defaults={
                    'is_debut_movie':is_debut_movie
                }
            )

            cast_details.roles.set(role_objects)

    # Create Ratings
    for rating_data in movie_rating_list:
        movie_id=rating_data["movie_id"]
        rating, created=Rating.objects.get_or_create(
            movie__movie_id=movie_id,
            defaults={
                'rating_one_count': rating_data.get("rating_one_count", 0),
                'rating_two_count': rating_data.get("rating_two_count", 0),
                'rating_three_count': rating_data.get("rating_three_count", 0),
                'rating_four_count': rating_data.get("rating_four_count", 0),
                'rating_five_count': rating_data.get("rating_five_count", 0),
            }
        )

        # Update Movie object with the rating
        Movie.objects.filter(movie_id=movie_id).update(rating=rating)


def get_no_of_distinct_movies_actor_acted(actor_id: Actor):
    """
    :param actor_id: 'actor_1'
    :return:
    Number of movies he/she acted
	Sample Output: 4
    """
    try:
        # First find the actor
        actor=Actor.objects.get(actor_id=actor_id)
        print(actor)
        # Get the required count
        count=Movie.objects.filter(cast__actors=actor).distinct().count()
        return count
    except Actor.DoesNotExist:
        return 0

def get_movies_directed_by_director(director_obj : Director):
    """
    :param director_obj: <Director: Director 1>
    :return:
    List of movie objects
    Sample Output: [<Movie: movie_1_obj>, <Movie: movie_2_obj>]
    """
    try:
        movies=list(Movie.objects.filter(director=director_obj).all())
        return movies
    except Exception as e:
        print(f"Exception: {e}")
        return []

def get_average_rating_of_movie(movie_obj: Movie):
    """
    :param movie_obj: <Movie: movie_1>
    :return:
    Average Rating
    Sample Output: 4.5
    """

    if movie_obj.rating is None:
        return 0
    rating_sum:float=0.0
    rating_sum+=movie_obj.rating.rating_one_count*1.0
    rating_sum+=movie_obj.rating.rating_two_count*2.0
    rating_sum+=movie_obj.rating.rating_three_count*3.0
    rating_sum+=movie_obj.rating.rating_four_count*4.0
    rating_sum+=movie_obj.rating.rating_five_count*5.0


    rating_average=rating_sum/get_total_number_of_ratings(movie_obj=movie_obj)

    return rating_average

def get_total_number_of_ratings(movie_obj: Movie):
    """
    :param movie_obj: <Movie: movie_1>
    :return:
    Average Rating
    Sample Output: 4.5
    """

    if movie_obj.rating is None:
        return 0
    rating_count: int = 0
    rating_count +=movie_obj.rating.rating_one_count
    rating_count +=movie_obj.rating.rating_two_count
    rating_count +=movie_obj.rating.rating_three_count
    rating_count +=movie_obj.rating.rating_four_count
    rating_count +=movie_obj.rating.rating_five_count

    return rating_count

def delete_movie_rating(movie_obj: Movie):
    try:
        if movie_obj.rating:
            rating=movie_obj.rating
            movie_obj.rating=None
            movie_obj.save()
            rating.delete()
        return 1
    except Exception as e:
        return e

def get_all_actor_objects_acted_in_given_movies(movie_objs: List[Movie]):
    actors_list=[]
    for movie in movie_objs:
        cast=Movie.objects.get(movie_id=movie.movie_id).cast
        cast_details=CastDetails.objects.filter(cast=cast)
        for detail in cast_details:
            if detail.actor not in actors_list:
                actors_list.append(detail.actor)
    return actors_list

def update_director_for_given_movie(movie_obj: Movie, director_obj: Director):
    try:
        movie_obj.director=director_obj
        movie_obj.save()
        return 1
    except Exception as e:
        return e

def get_distinct_movies_acted_by_actor_whose_name_contains_john():
    movies=[]
    actor_objs=Actor.objects.filter(name__contains="john")
    for actor_obj in actor_objs:
#         Get the CastDetails in which this actor is present
        cast_details=CastDetails.objects.filter(actor=actor_obj)

        for detail in cast_details:
            cast=detail.cast
#             Get movie with this cast
            movie=Movie.objects.get(cast=cast)
            if movie not in movies:
                movies.append(movie)
    return movies

def remove_all_actors_from_given_movie(movie_obj:Movie):
    # Get the cast, castdetails
    try:
        cast=movie_obj.cast
        cast_details=CastDetails.objects.filter(cast=cast)
        movie_obj.cast=None
        movie_obj.save()
        for detail in cast_details:
            detail.delete()

        if cast:
            cast.delete()
        return 1
    except Exception as e:
        return e

def get_all_rating_objects_for_given_movies(movie_objs: List[Movie]):
    ratings=[]
    for movie_obj in movie_objs:
        if movie_obj.rating:
            ratings.append(movie_obj.rating)

    return ratings

# IMDB 1 starts

def get_movies_by_given_movie_names(movie_names:List[str]):
    try:
        result=[]
        for movie in movie_names:
            movie_obj=Movie.objects.get(name=movie)
            movie_payload={}
            cast_payload_list=[]
    #         Get all cast_details
            cast_details=CastDetails.objects.filter(cast=movie_obj.cast)
            for detail in cast_details:
                for role in detail.roles.all():
                    actor_payload={
                        "actor":{
                            "name":detail.actor.name,
                            "actor_id":detail.actor.id
                        },
                        "role":role,
                        "is_debut_movie":detail.is_debut_movie
                    }
    #                 Append each role(actor_payload) to cast_payload_list
                    cast_payload_list.append(actor_payload)

    #         Update the movie payload
            movie_payload={
                "movie_id":movie_obj.movie_id,
                "name":movie_obj.name,
                "cast":cast_payload_list,
                "box_office_collection_in_crores":movie_obj.box_office_collection_in_crores,
                "release_date":movie_obj.release_date,
                "average_rating":get_average_rating_of_movie(movie_obj),
                "total_number_of_ratings":get_total_number_of_ratings(movie_obj=movie_obj)
            }

    except Exception as e:
        return e