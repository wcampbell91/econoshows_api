from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from econoshows_api.models import Band, Genre


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for user"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class BandSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for bands"""
    
    user = UserSerializer(many=False)

    class Meta: 
        model = Band
        url = serializers.HyperlinkedIdentityField(
            view_name='band', lookup_field='id'
        )
        fields = ('id', 'user', 'band_name','user_type', 'lineup', 'links', 'bio')
        depth = 1

class Bands(ViewSet):
    """Request handlers for Bands in EconoShows"""
    
    def list(self, request):
        bands = Band.objects.all()
        
        #add FILTERING here

        serializer = BandSerializer( bands, many=True, context={'request': request})
        return Response(serializer.data)
