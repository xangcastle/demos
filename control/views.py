from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import *


class Index(TemplateView):
    template_name = "control/index.html"
    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['apps'] = get_aplications(self.request.user)
        context['options'] = get_options(self.request.user)
        return context


class Calculator(TemplateView):
    template_name = "control/calculator.html"
