# See https://stackoverflow.com/questions/6560182/django-authentication-without-a-password for a good tutorial

from django.contrib.auth.backends import ModelBackend
from rsvp.models import PartyModel


class PasswordOnlyAuthBackend(ModelBackend):
    """Log into rsvp with only the password"""

    def authenticate(self, request, password=None, **kwargs):
        try:
            return PartyModel.objects.get(password=password)
        except PartyModel.DoesNotExist:
            return None

    def get_user(self, password):
        try:
            return PartyModel.objects.get(password=password)
        except PartyModel.DoesNotExist:
            return None

