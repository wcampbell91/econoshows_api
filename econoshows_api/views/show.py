from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status, permissions
from econoshows_api.models import Band, Genre, Venue, Show, ShowBand, ShowVenue


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.band.user == request.user or obj.venue.user == request.user

class Shows(ViewSet):
    """Request Handlers for Shows in EconoShows"""
    permission_classes = [ IsOwnerOrReadOnly ]
    
    def list(self, request):
        shows = Show.objects.all()

        # Add filtering here

        serializer = ShowSerializer(shows, many=True, context={'request': request})
        return Response(serializer.data)



class VenueOnShowSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Venue
        fields = ('id', 'venue_name', 'address', 'website', 'photos')


class BandOnShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Band
        fields = ('id', 'band_name', 'links', 'photos')

class ShowBandSerializer(serializers.ModelSerializer):
    
    band = BandOnShowSerializer(many=False)
    class Meta:
        model = ShowBand
        fields = ('id', 'band')
        depth = 1

class ShowVenueSerializer(serializers.ModelSerializer):

    venue = VenueOnShowSerializer(many=False)
    class Meta:
        model = ShowVenue
        fields = ('id', 'venue')
        depth = 1


class ShowSerializer(serializers.ModelSerializer):

    bands = ShowBandSerializer(many=True)
    venue = ShowVenueSerializer(many=True)
    class Meta:
        model = Show
        # url = serializers.HyperlinkedIdentityField(
        #     view_name='show', lookup_field='id'
        # )
        fields = ('id', 'title', 'bands', 'venue', 'description','date', 'door_time', 'show_time', 'cover','is_all_ages')
        depth = 1
