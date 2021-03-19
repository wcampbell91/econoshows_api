import base64
from django.core.files.base import ContentFile
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status, permissions
from econoshows_api.models import Band, Venue, Show, ShowBand, ShowVenue, show


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
        
        

class Shows(ViewSet):
    """Request Handlers for Shows in EconoShows"""
    permission_classes = [ IsOwnerOrReadOnly ]


    def list(self, request):
        shows = Show.objects.all()

        # Add filtering here

        serializer = ShowSerializer(shows, many=True, context={'request': request})
        return Response(serializer.data)


    def create(self, request):
        """Handle POST request on Shows"""

        new_show = Show()
        new_show.author = User.objects.get(pk=request.auth.user.id)
        new_show.title = request.data['title']
        new_show.description = request.data['description']
        new_show.door_time = request.data['door_time']
        new_show.show_time = request.data['show_time']
        new_show.cover = request.data['cover']
        new_show.date = request.data['date']

        if "poster" in request.data and request.data['poster'] is not None:
            format, imgstr = request.data['poster'].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f"{new_show.id}-{request.data['venue_name']}.{ext}")

            new_show.poster = data
        else:
            new_show.poster = None


        new_venue = ShowVenue()
        new_venue.venue = Venue.objects.get(pk=request.data['venue'])        
        new_show.is_all_ages = new_venue.venue.is_all_ages
        new_show.save()
        
        new_venue.show = new_show
        new_venue.save()

        # the request.data['bands'] MUST be a list when it comes in, 
        # may cause problems with front end
        for band_id in request.data['bands']:
            new_band = ShowBand()
            new_band.band = Band.objects.get(pk=band_id)
            new_band.show = new_show            
            new_band.save()
        
        try:
            serializer = ShowSerializer(new_show, many=False, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def update(self, request, pk=None):
        """Handle PUT requests for a show"""
        
        updated_show = Show.objects.get(pk=pk)
        updated_show.title = request.data['title']
        updated_show.description = request.data['description']
        updated_show.door_time = request.data['door_time']
        updated_show.show_time = request.data['show_time']
        updated_show.cover = request.data['cover']
        updated_show.date = request.data['date']

        if "poster" in request.data and request.data['poster'] is not None:
            format, imgstr = request.data['poster'].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f"{updated_show.id}-{request.data['venue_name']}.{ext}")

            updated_show.poster = data
        else:
            updated_show.poster = None

        show_venue = ShowVenue.objects.get(show=pk)
        show_venue.venue = Venue.objects.get(pk=request.data['venue'])
        updated_show.is_all_ages = show_venue.venue.is_all_ages
        self.check_object_permissions(request, updated_show)
        show_venue.save()

        for band_id in request.data['bands']:
            show_bands = ShowBand.objects.filter(show=pk)
            for show_band in show_bands:
                if show_band.band.id not in request.data['bands']:
                    show_band.delete()
                elif show_band.band.id != band_id:
                    show_band.band = Band.objects.get(pk=band_id)
                    self.check_object_permissions(request, updated_show)
                    show_band.save()

        self.check_object_permissions(request, updated_show)
        updated_show.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk=None):
        try:
            show = Show.objects.get(pk=pk)
            # self.check_object_permissions(request, show)
            show.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        except Show.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def retrieve(self, request, pk=None):
        """Handle GET reqeusts for single show"""
        try:
            show = Show.objects.get(pk=pk)
            serializer = ShowSerializer(show, many=False, context={'request': request})
            return Response(serializer.data)
        except Show.DoesNotExist as ex:
            return Response(
                {"message": "The requested Show does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return HttpResponseServerError(ex)


class VenueOnShowSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Venue
        fields = ('id', 'venue_name', 'address', 'website', 'photos')


class BandOnShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Band
        fields = ('id', 'band_name', 'links', 'photos')


class ShowBandSerializer(serializers.ModelSerializer):
    
    # band = BandOnShowSerializer(many=False)
    class Meta:
        model = ShowBand
        fields = ('id', 'band')
        depth = 1


class ShowVenueSerializer(serializers.ModelSerializer):

    venue = VenueOnShowSerializer(many=False)
    class Meta:
        model = ShowVenue
        fields = ('id', 'venue')


class ShowSerializer(serializers.ModelSerializer):

    bands = ShowBandSerializer(many=True)
    venue = ShowVenueSerializer(many=True)
    class Meta:
        model = Show
        fields = ('id', 'author', 'title', 'bands', 'venue', 'description','date', 'door_time', 'show_time', 'cover','is_all_ages')
        depth = 1
