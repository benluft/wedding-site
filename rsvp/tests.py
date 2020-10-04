from django.test import TransactionTestCase
from rsvp.models import GuestsModel, PartyModel, PASSWORD_LENGTH
from django.core.management import call_command
from django.db.utils import IntegrityError
from django.db import transaction
import os

# Create your tests here.


class GuestAndPartyModelTestCase(TransactionTestCase):
    def setUp(self):
        party_model = PartyModel.objects.create(name="The Incredibles")
        guest_model = GuestsModel.objects.create(first_name="Mr.", last_name="Incredible", party=party_model)

    def test_guest_and_party(self):
        """ Test basic functionality of guest and party models """

        party = PartyModel.objects.get(name="The Incredibles")
        guest = GuestsModel.objects.get(party=party)
        assert(guest.first_name == "Mr.")
        assert(guest.last_name == "Incredible")
        assert(len(party.invitation_password) == PASSWORD_LENGTH)
        assert(guest.party.name == "The Incredibles")
        assert(guest.get_party_name() == "The Incredibles")


    def test_import_command(self):
        """ Test the import admin command """

        opts = os.path.join(os.getcwd(), r"rsvp/management/test_guest_list.csv")
        call_command('import_guest_csv', opts)
        guest = GuestsModel.objects.get(first_name="Fred")
        assert(guest.last_name == "Flinstone")
        assert(guest.party == PartyModel.objects.get(name="The Flinstones"))
        party = PartyModel.objects.get(name="The Wicks")
        assert(party.email is None)
        all_guests_count = len(GuestsModel.objects.all())
        # There are 8 entries in the csv and 1 more for Mr. Incredible in test_guest_and_party
        assert(all_guests_count == 9)
        all_parties_count = len(PartyModel.objects.all())
        # 3 parties CSV, 1 added in test_guest_and_party
        assert(all_parties_count == 4)

    def test_duplicates(self):

        with self.assertRaises(IntegrityError):
            PartyModel.objects.create(name="The Incredibles")
        party_model = PartyModel.objects.get(name="The Incredibles")
        with self.assertRaises(IntegrityError):
            GuestsModel.objects.create(first_name="Mr.", last_name="Incredible", party=party_model)







