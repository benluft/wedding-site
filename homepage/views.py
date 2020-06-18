from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from . import models

page_nav_dict = {"Welcome": "landingpage:landing",
                 "RSVP": "landingpage:rsvp",
                 "Registry": "landingpage:landing",
                 "Find our Location": "landingpage:landing"}


class LandingPage(generic.TemplateView):

    template_name = r'homepage/landingpage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['page_names'] = page_nav_dict
        return context

class RSVPPage(generic.TemplateView):

    template_name = r'homepage/rsvp.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['page_names'] = page_nav_dict
        return context

# Create your views here.
