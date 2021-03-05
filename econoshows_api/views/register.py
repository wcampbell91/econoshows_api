"""Register User"""
import json
from django.http import HttpResponse, HttpResponseNotAllowed
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authtoken.models import Token
from econoshows_api.models import Band, Venue, Genre

@csrf_exempt
def login_user(request):
    '''login function'''
    body = request.body.decode('utf-8')
    req_body = json.loads(body)

    if request.method == "POST":
        name = req_body['username']
        pass_word = req_body['password']
        authenticated_user = authenticate(username=name, password=pass_word)

        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)
            data = json.dumps({"valid": True, "token": token.key, "id": authenticated_user.id})
            return HttpResponse(data, content_type='application/json')

        else:
            data = json.dumps({"valid": False})
            return HttpResponse(data, content_type='application/json')

    return HttpResponseNotAllowed(permitted_methods=['POST'])


@csrf_exempt
def register_band(request):
    """Register a band"""
    req_body = json.loads(request.body.decode())

    new_user = User.objects.create_user(
        username=req_body['username'],
        email=req_body['email'],
        password=req_body['password'],
        first_name=req_body['first_name'],
        last_name=req_body['last_name'],
        is_staff=True
    )

    band = Band.objects.create(
        band_name = req_body['band_name'],
        genre = Genre.objects.get(pk=req_body['genre']),
        links = req_body['links'],
        lineup = req_body['lineup'],
        photos = req_body['photos'],
        bio = req_body['bio'],
        user = new_user,
        user_type = 'band'
    )
    # TRY AGAIN WITH GENRE WHEN VIEW IS DONE!!

    band.save()

    token = Token.objects.create(user=new_user)

    data = json.dumps({"token": token.key, "id": new_user.id})
    return HttpResponse(data, content_type="application/json", status=status.HTTP_201_CREATED)

@csrf_exempt
def register_venue(request):
    """Register a venue"""
    req_body = json.loads(request.body.decode())

    new_user = User.objects.create_user(
        username = req_body['username'],
        email=req_body['email'],
        password = req_body['password'],
        first_name = req_body['first_name'],
        last_name = req_body['last_name']
    )

    venue = Venue.objects.create(
        venue_name = req_body['venue_name'],
        address = req_body['address'],
        booking_info = req_body['booking_info'],
        is_all_ages = req_body['is_all_ages'],
        has_backline = req_body['has_backline'],
        description = req_body['description'],
        website = req_body['website'],
        photos = req_body['photos'],
        user = new_user,
        user_type = 'venue'
    )

    venue.save()

    token = Token.objects.create(user=new_user)
    
    data = json.dumps({"token": token.key, "id": new_user.id})
    return HttpResponse(data, content_type = 'application/json')
