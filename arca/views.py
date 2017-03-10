from django.shortcuts import render
from .models import *

def login_app(request):
   usuario = None

   if request.method == "POST":
      username = request.POST.get('username', '')
      password = request.POST.get('password', '')
      usuario = autenticate(Usuario(), username, password)

   response = render(request, 'arca2/app.html', {"usuario" : usuario})
   if usuario:
      response.set_cookie('usuario', usuario)

   return response


def index_app(request):
   if 'usuario' in request.COOKIES:
      usuario = request.COOKIES['usuario']

      response = render(request, 'arca2/app.html', {"usuario" : usuario})

   else:
      response = render(request, 'arca2/app.html', {})

   return response


def login_comercio(request):
   comercio = None

   if request.method == "POST":
      username = request.POST.get('username', '')
      password = request.POST.get('password', '')
      comercio = autenticate(Comercio(), username, password)

   response = render(request, 'arca2/comercio.html', {"comercio" : comercio})
   if usuario:
      response.set_cookie('comercio', comercio)

   return response


def index_comercio(request):
   if 'comercio' in request.COOKIES:
      comercio = request.COOKIES['comercio']

      response = render(request, 'arca2/app.html', {"comercio" : comercio})

   else:
      response = render(request, 'arca2/comercio.html', {})
