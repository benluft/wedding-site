from django.forms import ModelForm
from django.views.generic import FormView, ListView

from homepage.views import WeddingPageContextMixin
from rsvp.models import PartyModel, GuestsModel
from rsvp.forms import PartyLoginForm, GuestRSVPForm, PartyRSVPForm

from extra_views import ModelFormSetView


# Create your views here.

class RSVPEnterPartyInfoView(WeddingPageContextMixin, ModelFormSetView):

    def get_navbar_focus(self):
        return "RSVP"

    template_name = r'rsvp/rsvp_party.html'
    model = PartyModel
    form_class = PartyRSVPForm
    factory_kwargs = {'extra': 0}

    def get_queryset(self):
        return super(RSVPEnterPartyInfoView, self).get_queryset().filter(id=self.request.session['party_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        party = PartyModel.objects.get(id=self.request.session['party_id'])
        context['party_name'] = party.party_name
        return context


class RSVPEnterGuestInfoView(WeddingPageContextMixin, ModelFormSetView):

    def get_navbar_focus(self):
        return "RSVP"

    template_name = r'rsvp/rsvp_guest.html'
    model = GuestsModel
    form_class = GuestRSVPForm
    factory_kwargs = {'extra': 0}
    success_url = '../enter_party_info/'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object_list = None

    def get_queryset(self):
        return super(RSVPEnterGuestInfoView, self).get_queryset().filter(party=self.request.session['party_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        party = PartyModel.objects.get(id=self.request.session['party_id'])
        context['party_name'] = party.party_name
        return context


class RSVPLogin(WeddingPageContextMixin, FormView):

    form_class = PartyLoginForm

    template_name = r'rsvp/rsvp_login.html'

    success_url = 'enter_guest_info/'

    def get_navbar_focus(self):
        return "RSVP"

    def form_valid(self, form):
        self.request.session['party_id'] = form.cleaned_data['party_id']
        return super().form_valid(form)


