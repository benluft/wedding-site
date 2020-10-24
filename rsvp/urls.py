from django.urls import path
from . import views

app_name = 'rsvppage'
urlpatterns = [
    path('', views.RSVPLogin.as_view(), name='rsvp'),
    path('enter_info/', views.RSVPEnterInfo.as_view(), name='rsvp_enter_info')
]
