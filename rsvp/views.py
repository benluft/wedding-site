from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View

from homepage.views import WeddingPageTemplateView


# Create your views here.
class RSVPLogin(WeddingPageTemplateView):

    template_name = r'rsvp/rsvp.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['current_page_name'] = "RSVP"
        return context


class RSVPPage(LoginRequiredMixin, View):
    login_url = '/add_rsvp/'
    redirect_field_name = '/rsvp/'
