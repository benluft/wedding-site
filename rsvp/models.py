from django.db import models
import uuid
from phonenumber_field.modelfields import PhoneNumberField

# TODO: Select the correct meal types
MEALS = ['Chicken', 'Vegetarian', 'Beef']


class Party(models.Model):
    """
    A party consists of one or mores guests
    """
    name = models.TextField()
    invitation_id = models.UUIDField(db_index=True, default=uuid.uuid4, unique=False)
    email = models.TextField(null=True)
    phone_number = PhoneNumberField(null=True)
    comments_or_questions = models.TextField(null=True)


class Guests(models.Model):
    """
    A guest for the wedding, belongs to a party
    """
    first_name = models.TextField()
    last_name = models.TextField()
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    is_attending = models.NullBooleanField(deafult=None)
    is_child = models.BooleanField(default=False)
    meal = models.CharField(max_length=20, choices=MEALS)

