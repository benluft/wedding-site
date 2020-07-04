from django.urls import path
from . import views

app_name = 'landingpage'
urlpatterns = [
    path('', views.LandingPage.as_view(), name='landing'),
    path('rsvp/', views.RSVPPage.as_view(), name='rsvp'),
    path('registry/', views.RegistryPage.as_view(), name='registry'),
    path('location/', views.FindOurLocationPage.as_view(), name='find_our_location')
]
