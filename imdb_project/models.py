from enum import unique

from django.db import models
from django.db.models import DateField, ForeignKey, OneToOneField, ManyToManyField, CASCADE, BooleanField, \
    PositiveIntegerField, CharField, FloatField


class Director(models.Model):
    name=CharField(max_length=100)

class Actor(models.Model):
    actor_id=CharField(max_length=100, primary_key=True)
    name=CharField(max_length=100)

class Role(models.Model):
    role_name=CharField(max_length=50, unique=True)

class CastDetails(models.Model):
    cast=ForeignKey('Cast', on_delete=models.CASCADE)
    actor=ForeignKey('Actor', on_delete=models.CASCADE)
    roles=ManyToManyField('Role')
    is_debut_movie=BooleanField()

    class Meta:
        unique_together=('cast','actor')

class Cast(models.Model):
    actors=ManyToManyField('Actor', through='CastDetails')


class Rating(models.Model):
    # Doubt - How can we make it scalable, or instead
    # we can have rating values and return seperate ratings by calculation

    rating_one_count=PositiveIntegerField(default=0)
    rating_two_count=PositiveIntegerField(default=0)
    rating_three_count=PositiveIntegerField(default=0)
    rating_four_count=PositiveIntegerField(default=0)
    rating_five_count=PositiveIntegerField(default=0)

class Movie(models.Model):
    name=CharField(max_length=100)
    movie_id=CharField(max_length=100, primary_key=True)
    release_date=DateField()
    box_office_collection_in_crores=FloatField()
    director=ForeignKey('Director', null=False, on_delete=models.CASCADE)
    cast=OneToOneField('Cast', null=True, on_delete=models.CASCADE)
    rating=OneToOneField('Rating', null=True, on_delete=models.CASCADE)



