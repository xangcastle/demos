from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class Index(TemplateView):
    template_name = "arca/index.html"
    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        return context



class Login(TemplateView):
    template_name = "arca/login.html"
    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        return context

    def post(self, *args, **kwargs):
        '''
        regreso un json al modal de login que se aiga abierto
        '''
        backend = request.POST.get('backend', '') # algun input hidden en el modal que nos de si es fb, tw, go
        cuenta = request.POST.get('cuenta', None)
        otrodato = request.POST.get('cuenta', None)

        if backend == "fb":
            pass

        if backend == "tw":
            pass

        if backend == "go":
            pass
