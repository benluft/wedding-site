from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.forms.models import BaseModelFormSet
from django.forms.utils import ErrorList
from django.utils.html import format_html

from rsvp.models import PASSWORD_LENGTH, PartyModel, GuestsModel





class PartyErrorList(ErrorList):

    def as_ul(self):
        return_string = ''
        for e in self:
            return_string += format_html('<strong>{}</strong>', e)
        return return_string


class PartyLoginForm(forms.Form):
    password = forms.CharField(max_length=PASSWORD_LENGTH, widget=forms.PasswordInput())

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=PartyErrorList,
                 label_suffix=None, empty_permitted=False, field_order=None, use_required_attribute=None,
                 renderer=None):
        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, field_order,
                         use_required_attribute, renderer)

    def clean_password(self):
        all_parties = PartyModel.objects.all()
        for party in all_parties:
            if party.check_password(self.cleaned_data['password']):
                self.cleaned_data['party_id'] = party.id
                return self.cleaned_data['password']
        raise ValidationError("Password is Incorrect")


class GuestRSVPForm(ModelForm):

    first_name = forms.CharField()
    last_name = forms.CharField()
    party = forms.CharField()
    id = forms.CharField()

    class Meta:
        model = GuestsModel
        fields = '__all__'

    def clean(self):
        return super().clean()

    def clean_is_attending(self):
        if self.cleaned_data['is_attending']:
            return self.cleaned_data['is_attending']
        else:
            raise ValidationError("Please Indicate whether each guest will be attending")

    def has_changed(self):
        changed_data = super().has_changed()
        return True


class PartyRSVPForm(ModelForm):
    confirm_email = forms.EmailField()

    class Meta:
        model = PartyModel
        fields = ['email', 'confirm_email', 'comments_or_questions']

