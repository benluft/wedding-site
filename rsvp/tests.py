from django.test import TestCase
from rsvp.models import GuestsModel, PartyModel, PASSWORD_LENGTH
from django.core.management import call_command
import os
from shutil import copyfile
# Create your tests here.


class GuestAndPartyModelTestCase(TestCase):
    def setUp(self):
        party_model = PartyModel.objects.create(party_name="The Incredibles")
        self.party_model_password = party_model.set_password()
        party_model.save()
        guest_model = GuestsModel.objects.create(first_name="Mr.", last_name="Incredible", party=party_model)

    def test_guest_and_party(self):
        """ Test basic functionality of guest and party models """

        party = PartyModel.objects.get(party_name="The Incredibles")
        guest = GuestsModel.objects.get(party=party)
        assert(guest.first_name == "Mr.")
        assert(guest.last_name == "Incredible")
        assert(party.check_password(self.party_model_password) is True)
        assert(guest.get_party_name() == "The Incredibles")

    def test_import_command(self):
        """ Test the import admin command """

        test_file = os.path.join(os.getcwd(), r"rsvp/management/test_guest_list.csv")
        tmp_file = os.path.join(os.path.dirname(test_file), "tmp_test_guest_list.csv")
        copyfile(test_file, tmp_file)
        opts = tmp_file
        call_command('import_guest_csv', opts)
        guest = GuestsModel.objects.get(first_name="Fred")
        assert(guest.last_name == "Flinstone")
        assert(guest.party.party_name == "The Flinstones")
        party = PartyModel.objects.get(party_name="The Wicks")
        assert(party.email is None)
        all_guests_count = len(GuestsModel.objects.all())
        # There are 8 entries in the csv and 1 more for Mr. Incredible in test_guest_and_party
        assert(all_guests_count == 15)
        all_parties_count = len(PartyModel.objects.all())
        # 6 parties CSV, 1 added in test_guest_and_party
        assert(all_parties_count == 7)
