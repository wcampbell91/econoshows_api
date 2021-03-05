from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from econoshows_api.models import Venue

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for user"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class VenueSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for bands"""
    
    user = UserSerializer(many=False)
    class Meta: 
        model = Venue
        fields = ('id', 'user', 'venue_name','user_type', 'address', 'booking_info', 'description', 'is_all_ages', 'has_backline', 'website')
        depth = 1


class Venues(ViewSet):
    """Request handler for Venues in the EconoShows platform"""
    def list(self, request):
        venues = Venue.objects.all()

        serializer = VenueSerializer(venues, many=True, context={'request': request})
        return Response(serializer.data)
