from django.db import models
import random
import string
from phonenumber_field.modelfields import PhoneNumberField

# TODO: Select the correct meal types
MEALS = [('CHICKEN', 'Chicken'),
         ('VEG', 'Vegetarian'),
         ('BEEF', 'Beef')]

PASSWORD_LENGTH = 15


def random_invitation_password():
    possible_chars = string.ascii_letters + string.digits
    for _ in range(100):
        password = ''.join(random.choice(possible_chars) for i in range(PASSWORD_LENGTH))
        if not PartyModel.objects.filter(invitation_password=password):
            return password
    raise ValueError("Could not pick a unique password, tried 100 times")


class PartyModel(models.Model):
    """
    A party consists of one or mores guests

    Must have a name, invitation password, and email OR phone number

    The invitation password is a 15 character random value

    """
    name = models.TextField()
    invitation_password = models.CharField(editable=False, unique=True, max_length=PASSWORD_LENGTH,
                                           default=random_invitation_password)
    email = models.TextField(null=True)
    phone_number = PhoneNumberField(null=True)
    comments_or_questions = models.TextField(null=True)


class GuestsModel(models.Model):
    """
    A guest for the wedding, belongs to a party
    """
    first_name = models.TextField()
    last_name = models.TextField()
    party = models.ForeignKey(PartyModel, on_delete=models.CASCADE)
    is_attending = models.NullBooleanField(default=None)
    is_child = models.BooleanField(default=False)
    meal = models.CharField(max_length=20, choices=MEALS)

