from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.views.generic.base import View
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from econoshows_api.models import Genre

class GenreSerializer(serializers.HyperlinkedModelSerializer):
    """JSON Serializer for Genre"""
    class Meta: 
        model = Genre
        url = serializers.HyperlinkedIdentityField(
            view_name="genre",
            lookup_field="id"
        )
        fields = ('id', 'name')


class Genres(ViewSet):
    """Request Handlers for Genres in EconoShows"""

    def list(self, request):
        genres = Genre.objects.all()

        serializer = GenreSerializer( genres, many=True, context={"request": request})
        return Response(serializer.data)
