from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
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
        """Handle GET requests for a Venue"""
        venues = Venue.objects.all()

        serializer = VenueSerializer(venues, many=True, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests for a Venue"""

        venue = Venue.objects.get(user=request.auth.user)
        venue.user.username = request.data['username']
        venue.user.first_name = request.data['first_name']
        venue.user.last_name = request.data['last_name']
        venue.user.email = request.data['email']
        venue.venue_name = request.data['venue_name']
        venue.address = request.data['address']
        venue.booking_info = request.data['booking_info']
        venue.description = request.data['description']
        venue.is_all_ages = request.data['is_all_ages']
        venue.has_backline = request.data['has_backline']
        venue.website = request.data['website']
        venue.photos = request.data['photos']
        
        venue.user.save()
        venue.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
