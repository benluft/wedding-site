import os
from rsvp.models import PartyModel, GuestsModel
from django.core.management.base import BaseCommand, CommandError
from django.db.models import ObjectDoesNotExist


class Command(BaseCommand):

    help = ("\n"
            "    Run in the same directory as a csv named test_guest_list.csv with the following 3 columns\n"
            "\n"
            "    party name, guest first name, guest last name\n"
            "\n"
            "    Note that the first line will simply be a header\n"
            "\n"
            "    if party is empty, the previous party will be used\n"
            "\n"
            "    ")

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str)

    def handle(self, *args, **options):
        if not os.path.exists(options['csv_path']):
            print('test_guest_list.csv was not found. Exiting')
            raise CommandError("Path {} does not exist".format(options['csv_path']))

        with open(options['csv_path']) as guest_csv:
            header_encountered = False
            current_party = None
            for line in guest_csv:
                if not header_encountered:
                    header_encountered = True
                    continue
                split_line = line.split(',')
                split_line = [field.strip() for field in split_line]
                if split_line[0] != "":
                    current_party = split_line[0]
                # Get or create returns a tuple, the first of which is the object, and the second of which is
                # true if created, or false if not created
                try:
                    party_model = PartyModel.objects.get(party_name=current_party)
                except ObjectDoesNotExist:
                    party_model = PartyModel.objects.create_user(party_name=current_party)
                guests_model = GuestsModel.objects.create(first_name=split_line[1], last_name=split_line[2], party=party_model)
                party_model.save()
                guests_model.save()
