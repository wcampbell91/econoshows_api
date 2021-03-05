from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status, permissions
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


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.user == request.user

class Venues(ViewSet):
    """Request handler for Venues in the EconoShows platform"""

    permission_classes= [ IsOwnerOrReadOnly ]

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

    def retrieve(self,request,pk=None):
        """Handle GET for single venue"""
        try:
            venue = Venue.objects.get(pk=pk, user=request.auth.user)
            serializer = VenueSerializer(venue, many=False, context={'request': request})
            return Response(serializer.data)
        except Venue.DoesNotExist as ex:
            return Response(
                {"mesage": "The requested venue does not exist, or you do not have permission to access it"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        try:
            venue = Venue.objects.get(pk=pk)
            user = User.objects.get(pk=request.auth.user.id)
            self.check_object_permissions(request, venue)
            venue.delete()
            user.delete()
            
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        except Venue.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
