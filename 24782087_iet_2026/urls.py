from django.http import HttpResponse
from django.urls import path
from django.views.debug import default_urlconf


def welcome(request):
    return HttpResponse("Selamat Datang")


urlpatterns = [
    path("", default_urlconf),
    path("welcome", welcome),
    path("welcome/", welcome),
]
