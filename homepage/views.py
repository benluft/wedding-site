from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from . import models
from abc import ABC


class WeddingPageTemplateView(generic.TemplateView):

    template_name = r'homepage/landingpage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['page_names'] = {"Welcome": "landingpage:landing",
                                 "RSVP": "landingpage:rsvp",
                                 "Registry": "landingpage:registry",
                                 "Find our Location": "landingpage:find_our_location"}
        return context


class LandingPage(WeddingPageTemplateView):

    template_name = r'homepage/landingpage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['current_page_name'] = "Welcome"
        return context


class RSVPPage(WeddingPageTemplateView):

    template_name = r'homepage/rsvp.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['current_page_name'] = "RSVP"
        return context


class RegistryPage(WeddingPageTemplateView):

    template_name = r'homepage/registry.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['current_page_name'] = "Registry"
        return context


class FindOurLocationPage(WeddingPageTemplateView):

    template_name = r'homepage/find_our_location.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['current_page_name'] = "Find our Location"
        return context

