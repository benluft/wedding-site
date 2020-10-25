from django.views.generic import FormView, ListView

from homepage.views import WeddingPageTemplateView
from rsvp.models import PartyModel, GuestsModel
from rsvp.forms import PartyLoginForm


# Create your views here.
class RSVPEnterInfo(WeddingPageTemplateView, ListView):
    template_name = r'rsvp/rsvp.html'
    model = GuestsModel

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object_list = None

    def get_queryset(self):
        objects = self.model.objects.filter(party=self.request.session['party_id'])
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page_name'] = "RSVP"
        party = PartyModel.objects.get(id=self.request.session['party_id'])
        context['party_name'] = party.party_name
        return context


class RSVPLogin(WeddingPageTemplateView, FormView):

    form_class = PartyLoginForm

    template_name = r'rsvp/rsvp_login.html'

    success_url = 'enter_info/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['current_page_name'] = "RSVP"
        return context

    def form_valid(self, form):
        self.request.session['party_id'] = form.cleaned_data['party_id']
        return super().form_valid(form)


