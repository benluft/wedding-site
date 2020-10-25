from django.forms import ModelForm
from django.views.generic import FormView, ListView

from homepage.views import WeddingPageContextMixin
from rsvp.models import PartyModel, GuestsModel
from rsvp.forms import PartyLoginForm, GuestRSVPForm

from extra_views import ModelFormSetView


# Create your views here.

class RSVPEnterInfo(WeddingPageContextMixin, ModelFormSetView):

    def get_navbar_focus(self):
        return "RSVP"

    template_name = r'rsvp/rsvp.html'
    model = GuestsModel
    form_class = GuestRSVPForm
    factory_kwargs = {'extra': 0}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object_list = None

    def get_queryset(self):
        return super(RSVPEnterInfo, self).get_queryset().filter(party=self.request.session['party_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        party = PartyModel.objects.get(id=self.request.session['party_id'])
        context['party_name'] = party.party_name
        return context


class RSVPLogin(WeddingPageContextMixin, FormView):

    form_class = PartyLoginForm

    template_name = r'rsvp/rsvp_login.html'

    success_url = 'enter_info/'

    def get_navbar_focus(self):
        return "RSVP"

    def form_valid(self, form):
        self.request.session['party_id'] = form.cleaned_data['party_id']
        return super().form_valid(form)


