from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class Index(TemplateView):
    template_name = "arca/index.html"
    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        return context
