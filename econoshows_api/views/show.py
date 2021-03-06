from econoshows_api.views.band import IsOwnerOrReadOnly
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status, permissions
from econoshows_api.models import Band, Genre, Venue

class Shows(ViewSet):
    """Request Handlers for Shows in EconoShows"""
    permission_classes = [ IsOwnerOrReadOnly ]
