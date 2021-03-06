from enum import auto
from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING
from .genre import Genre
from django.contrib.auth.models import User

class Show(models.Model):
    author = models.OneToOneField(User, on_delete=DO_NOTHING, null=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    door_time = models.TimeField(auto_now=False, auto_now_add=False)
    show_time = models.TimeField(auto_now=False, auto_now_add=False)
    cover = models.CharField(max_length=20)
    date = models.DateField(auto_now=False, default="0000-00-00")
    is_all_ages = models.BooleanField(default=False)
    genre = models.ForeignKey(Genre, on_delete=DO_NOTHING, related_name="shows")
    poster = models.ImageField(upload_to='show_posters', height_field=None, width_field=None, max_length=None, null=True)
