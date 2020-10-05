from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from homepage.views import WeddingPageTemplateView
from rsvp.models import PartyModel
from rsvp.forms import PartyLoginForm
from rsvp import urls


# Create your views here.
class RSVPEnterInfo(WeddingPageTemplateView):

    template_name = r'rsvp/rsvp.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['current_page_name'] = "RSVP"
        return context


class RSVPLogin(WeddingPageTemplateView, FormView):

    form_class = PartyLoginForm

    template_name = r'rsvp/rsvp_login.html'

    success_url = 'rsvp/enter_info/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['current_page_name'] = "RSVP"
        return context

    def form_valid(self, form):
        all_parties = PartyModel.objects.all()
        for party in all_parties:
            if party.check_password(form.cleaned_data['password']):
                print("yay")
                return super().form_valid(form)


