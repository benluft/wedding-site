import os

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from rsvp.models import PartyModel, GuestsModel
from django.core.management.base import BaseCommand, CommandError


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
            raise CommandError('test_guest_list.csv was not found. Exiting')
        dirname = os.path.dirname(options['csv_path'])
        output_csv_path = os.path.join(dirname, "csv_with_passwords.csv")
        if not os.path.exists(output_csv_path):
            with open(output_csv_path, "w") as output_f:
                output_f.write("Party,First Name,Last Name,Password\n")
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
                    party_model = PartyModel.objects.create(party_name=current_party)
                    plaintext_password = party_model.set_password()
                else:
                    party_model = PartyModel.objects.get(party_name=current_party)
                try:
                    GuestsModel.objects.create(first_name=split_line[1], last_name=split_line[2], party=party_model)
                except ValidationError:
                    continue

                # Write a csv to show the passwords that can be used in the invitations
                with open(output_csv_path, 'a') as csv_write:
                    no_newline_line = line.replace('\n', '')
                    csv_write.write(no_newline_line)
                    if split_line[0] != "":
                        csv_write.write(",{}".format(plaintext_password))
                    csv_write.write("\n")
        os.remove(options['csv_path'])

