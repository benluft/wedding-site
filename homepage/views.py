from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.views.generic.base import ContextMixin, TemplateView

from . import models
from abc import ABC, abstractmethod


class WeddingPageContextMixin(ContextMixin):

    template_name = r'homepage/landingpage.html'

    @abstractmethod
    def get_navbar_focus(self):
        return "Welcome"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_names'] = {"Welcome": "landingpage:landing",
                                 "RSVP": "rsvppage:rsvp",
                                 "Registry": "landingpage:registry",
                                 "Find our Location": "landingpage:find_our_location"}
        if self.get_navbar_focus() not in context['page_names']:
            raise ValueError("{} is not in page names".format(self.get_navbar_focus()))
        context['current_page_name'] = self.get_navbar_focus()
        return context


class LandingPage(WeddingPageContextMixin, TemplateView):

    template_name = r'homepage/landingpage.html'

    def get_navbar_focus(self):
        return "Welcome"


class RegistryPage(WeddingPageContextMixin, TemplateView):

    template_name = r'homepage/registry.html'

    def get_navbar_focus(self):
        return "Registry"


class FindOurLocationPage(WeddingPageContextMixin, TemplateView):

    template_name = r'homepage/find_our_location.html'

    def get_navbar_focus(self):
        return "Find our Location"


