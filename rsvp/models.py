from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import check_password, is_password_usable, make_password
from django.db.utils import IntegrityError

PASSWORD_LENGTH = 15


class PartyManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, party_name, password=None, **extra_fields):
        if not party_name:
            raise ValueError("The Party Name must be set")
        if password is None:
            password_encoded = make_password(self.make_random_password(PASSWORD_LENGTH))
        else:
            password_encoded = make_password(password)
        party = self.model(party_name=party_name, password=password_encoded, **extra_fields)
        party.save()
        return party

    def create_user(self, party_name, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(party_name, **extra_fields)

    def create_superuser(self, party_name, password, **extra_fields):
        print("Party name is {}, password is {}".format(party_name, password))
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(party_name, password, **extra_fields)


class PartyModel(AbstractBaseUser, PermissionsMixin):
    """
    A party consists of one or mores guests

    Must have a name, invitation password, and email OR phone number

    The invitation password is a 15 character random value

    """
    party_name = models.TextField(unique=True)
    password = models.CharField(max_length=128, unique=True)
    email = models.EmailField(blank=True)
    comments_or_questions = models.TextField(null=True, blank=True)

    objects = PartyManager()

    USERNAME_FIELD = 'password'
    REQUIRED_FIELDS = ['party_name']


class GuestsModel(models.Model):
    """
    A guest for the wedding, belongs to a party
    """
    first_name = models.TextField()
    last_name = models.TextField()
    party = models.ForeignKey(PartyModel, on_delete=models.CASCADE)
    is_attending = models.NullBooleanField(default=None)

    class Meta:
        unique_together = ['first_name', 'last_name', 'party']

    def get_party_name(self):
        return self.party.party_name
