from django.db import models
from django.db.models.fields import CharField

class Genre(models.Model):
    name = CharField(max_length=20)
