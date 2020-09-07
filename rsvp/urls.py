from django.urls import path
from . import views

app_name = 'rsvppage'
urlpatterns = [
    path('', views.RSVPPage.as_view(), name='rsvp'),
]
