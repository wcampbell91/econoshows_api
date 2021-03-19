import base64
from econoshows_api.models.show import Show
from econoshows_api.views.show import ShowVenueSerializer
from django.core.files.base import ContentFile
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status, permissions
from econoshows_api.models import Band, Genre


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for user"""
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email']


class BandGenreSerializer(serializers.ModelSerializer):
    """JSON serializer for genres on band"""

    class Meta:
        model = Genre
        fields = ('id', 'name')

# class ShowDetailSerializer(serializers.HyperlinkedModelSerializer):

#     venue = ShowVenueSerializer(many=True)
#     class Meta:
#         model = Show
#         fields = ('id', 'title', 'venue','date')
        

# class BandShowSerializer(serializers.HyperlinkedModelSerializer):
    
#     show = ShowDetailSerializer(many=False)
#     class Meta: 
#         model = ShowBand
#         fields = ('id', 'show')

class BandSerializer(serializers.ModelSerializer):
    """JSON serializer for bands"""
    
    user = UserSerializer(many=False)
    genre = BandGenreSerializer(many=False)
    # shows = BandShowSerializer(many=True)
    class Meta: 
        model = Band
        fields = ('id', 'user', 'band_name', 'genre', 'user_type', 'lineup', 'links', 'bio', 'shows')
        depth = 1


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True


class Bands(ViewSet):
    """Request handlers for Bands in EconoShows"""

    permission_classes=[ IsOwnerOrReadOnly ]
    
    def list(self, request):
        bands = Band.objects.all()
        
        #add FILTERING here

        serializer = BandSerializer( bands, many=True, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests for a band"""
        band = Band.objects.get(user=request.auth.user)
        band.user.username = request.data['username']
        band.user.first_name = request.data['first_name']
        band.user.last_name = request.data['last_name']
        band.user.email = request.data['email']
        band.band_name = request.data['band_name']
        band.genre = Genre.objects.get(pk=request.data['genre'])
        band.lineup = request.data['lineup']
        band.links = request.data['links']
        band.bio = request.data['bio']

        if "photos" in request.data and request.data['photos'] is not None:
            format, imgstr = request.data['poster'].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f"{band.id}-{request.data['band_name']}.{ext}")

            band.photos = data

        band.user.save()
        band.save()
        
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single band"""
        try:
            band = Band.objects.get(pk=pk)
            serializer = BandSerializer(band, many=False, context={'request': request})
            return Response(serializer.data)
        except Band.DoesNotExist as ex:
            return Response(
                {'message': "The requested band does not exist, or you do not have permission to access it"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        try:
            band = Band.objects.get(pk=pk)
            user = User.objects.get(pk=request.auth.user.id)
            self.check_object_permissions(request, band)
            band.delete()
            user.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Band.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
