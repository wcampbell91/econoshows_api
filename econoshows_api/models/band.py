from django.db import models
from django.contrib.auth.models import User
from .genre import Genre
from datetime import date
class Band(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    user_type = models.CharField(max_length=20)
    band_name = models.CharField(max_length=50)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='bands', null=True)
    lineup = models.CharField(max_length=20)
    links = models.CharField(max_length=200)
    photos = models.ImageField(upload_to='bands', height_field=None, width_field=None, max_length=None, null=True)
    bio = models.CharField(max_length=500, default="")
