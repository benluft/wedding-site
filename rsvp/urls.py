from django.urls import path
from . import views

app_name = 'rsvppage'
urlpatterns = [
    path('', views.RSVPLogin.as_view(), name='rsvp'),
    path('enter_guest_info/', views.RSVPEnterGuestInfoView.as_view(), name='rsvp_enter_guest_info'),
    path('enter_party_info/', views.RSVPEnterPartyInfoView.as_view(), name='rsvp_enter_party_info')
]
