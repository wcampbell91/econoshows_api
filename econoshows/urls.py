"""econoshows URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from econoshows_api.views.register import register_band, register_venue
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from django.conf import settings
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from econoshows_api.models import *
from econoshows_api.views import *


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'bands', Bands, 'band')
router.register(r'venues', Venues, 'venue')
router.register(r'genres', Genres, 'genre')
router.register(r'shows', Shows, 'show')



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('register_band', register_band),
    path('register_venue', register_venue),
    path('login', login_user)
]
