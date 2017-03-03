import json

from arca.models import *
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class Index(TemplateView):
    template_name = "arca/base1.html"
    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        return context

def get_comercio_categorias(request):
    categorias = Comercio_Categoria.objects.all()
    data = []
    for categoria in categorias:
        obj_json = {}
        obj_json['id'] = categoria.id
        obj_json['nombre'] = categoria.nombre
        data.append(obj_json)

    data = json.dumps(data)
    response = HttpResponse(data, content_type='application/json')
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


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
