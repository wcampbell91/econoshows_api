from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import DO_NOTHING

class Venue(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    user_type = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    booking_info = models.CharField(max_length=50)
    is_all_ages = models.BooleanField(default=False)
    has_backline = models.BooleanField(default=False)
    photos = models.ImageField(upload_to="venues", height_field=None, width_field=None, max_length=None, null=True)
