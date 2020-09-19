from django.urls import path
from . import views

app_name = 'rsvppage'
urlpatterns = [
    path('', views.RSVPLogin.as_view(), name='rsvp'),
]
