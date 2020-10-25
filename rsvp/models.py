from django.core.exceptions import ValidationError
from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password, check_password

PASSWORD_LENGTH = 15


class PartyModel(models.Model):
    """
    A party consists of one or mores guests

    Must have a name, invitation password, and email OR phone number

    The invitation password is a 15 character random value

    """
    party_name = models.TextField()
    _password = models.CharField(editable=False, max_length=128)
    email = models.EmailField(null=True)
    comments_or_questions = models.TextField(null=True)

    def set_password(self):
        password_tuple = random_invitation_password()
        self._password = password_tuple[1]
        self.save()
        return password_tuple[0]

    def check_password(self, password):
        return check_password(password, self._password)


def random_invitation_password():
    for _ in range(100):
        password = get_random_string(length=PASSWORD_LENGTH,
                                     allowed_chars='abcdefghjkmnpqrstuvwxyz'
                                                   'ABCDEFGHJKLMNPQRSTUVWXYZ'
                                                   '23456789')
        identical_password_found = False
        for party_model in PartyModel.objects.all():
            if party_model.check_password(password):
                identical_password_found = True
                break
        if not identical_password_found:
            return password, make_password(password)
    raise ValueError("Could not pick a unique password, tried 100 times")


class GuestsModel(models.Model):
    """
    A guest for the wedding, belongs to a party
    """
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    party = models.ForeignKey(PartyModel, on_delete=models.CASCADE)
    is_attending = models.NullBooleanField(default=None)

    def get_party_name(self):
        return self.party.party_name

    def validate_unique(self, exclude=None):
        # find all guests that have the current first name and last name
        guest_models = GuestsModel.objects.filter(first_name=self.first_name, last_name=self.last_name)
        for guest_model in guest_models:
            party_model = PartyModel.objects.get(party_name=guest_model.party.party_name)
            if party_model:
                raise ValidationError("Guest with the same first, last, and party name found")
            party_model = PartyModel.objects.get(pk=guest_model.party.id)
            if party_model:
                raise ValidationError("Guest with same first, last and party id found")

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(GuestsModel, self).save(*args, **kwargs)