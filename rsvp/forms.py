from django import forms
from rsvp.models import PASSWORD_LENGTH


class PartyLoginForm(forms.Form):
    password = forms.CharField(max_length=PASSWORD_LENGTH, widget=forms.PasswordInput())
