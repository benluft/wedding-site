import os
from rsvp.models import PartyModel, GuestsModel
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    help = ("\n"
            "    Run in the same directory as a csv named guest_list.csv with the following 3 columns\n"
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
            print('guest_list.csv was not found. Exiting')
            raise CommandError

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
                party_model_tuple = PartyModel.objects.get_or_create(name=current_party)
                guests_model = GuestsModel.objects.create(first_name=split_line[1], last_name=split_line[2], party=party_model_tuple[0])
                party_model_tuple[0].save()
                guests_model.save()
