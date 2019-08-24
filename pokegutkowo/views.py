# Create your views here.
from django.views.generic import TemplateView

from pokegutkowo.models import Players, Post, Settings


class IndexView(TemplateView):
    template_name = 'index.html'

