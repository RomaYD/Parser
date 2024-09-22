from django.db import models


class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=255, null=True)
    year = models.IntegerField(null=True)
    description = models.TextField(null=True)
    rating = models.CharField(max_length=255, null=True)
    short_description = models.TextField(null=True)
    leanght = models.CharField(max_length=255, null=True)
    age_rating = models.IntegerField(null=True)
    genres = models.TextField(null=True)
    actors = models.TextField(null=True)
    composers = models.TextField(null=True)
    designers = models.TextField(null=True)
    directors = models.TextField(null=True)
    editors = models.TextField(null=True)
    operators = models.TextField(null=True)
    producers = models.TextField(null=True)
    writers = models.TextField(null=True)
    voice_actors = models.TextField(null=True)


    def __str__(self):
        return self.id