from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from rsvp.models import GuestsModel, PartyModel

# Register your models here.


class GuestInline(admin.TabularInline):
    model = GuestsModel


class PartyAdmin(admin.ModelAdmin):
    list_display = ('party_name', 'email', 'guests_attending')
    inlines = [GuestInline]

    def guests_attending(self, obj):
        guests = GuestsModel.objects.filter(party=obj)
        attending_count = 0
        for guest in guests:
            if guest.is_attending:
                attending_count += 1
        return "{}/{}".format(attending_count, len(guests))


admin.site.register(PartyModel, PartyAdmin)