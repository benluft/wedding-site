# Generated by Django 3.0.8 on 2020-10-25 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0002_auto_20201004_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guestsmodel',
            name='first_name',
            field=models.TextField(editable=False),
        ),
        migrations.AlterField(
            model_name='guestsmodel',
            name='last_name',
            field=models.TextField(editable=False),
        ),
    ]
