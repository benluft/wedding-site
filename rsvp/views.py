from django.shortcuts import render

from homepage.views import WeddingPageTemplateView


# Create your views here.
class RSVPLogin(WeddingPageTemplateView):

    template_name = r'rsvp/rsvp.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['current_page_name'] = "RSVP"
        return context
