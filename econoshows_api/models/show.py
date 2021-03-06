from enum import auto
from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.contrib.auth.models import User

class Show(models.Model):
    author = models.ForeignKey(User, on_delete=DO_NOTHING, null=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    door_time = models.TimeField(auto_now=False, auto_now_add=False)
    show_time = models.TimeField(auto_now=False, auto_now_add=False)
    cover = models.CharField(max_length=20)
    date = models.DateField(auto_now=False, default="0000-00-00")
    is_all_ages = models.BooleanField(default=False)
    poster = models.ImageField(upload_to='show_posters', height_field=None, width_field=None, max_length=None, null=True)
    bands = models.ManyToManyField("Band", related_name="shows", related_query_name="show")
    venue = models.ForeignKey("Venue", related_name="shows", related_query_name="show", on_delete=models.DO_NOTHING)
