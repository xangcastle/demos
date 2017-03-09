import json

from django import forms

from arca.models import *
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from inblensa.models import Profile
from social_django import *
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView
from social_django.models import UserSocialAuth


class Login(TemplateView):
    template_name = "arca/login.html"

    def get(self, request, *args, **kwargs):

        next_page = request.GET.get('next', '/arca/')
        if request.user.is_authenticated():
            return redirect(next_page)
        else:
            context = super(Login, self).get_context_data(**kwargs)
            return super(Login, self).render_to_response(context)


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


class account_profile(TemplateView):
    template_name = "arca/account_profile.html"

    def get(self, request, *args, **kwargs):
        if not request.user.profile:
            Profile.objects.get_or_create(user=request.user)

        context = super(account_profile, self).get_context_data(**kwargs)
        return super(account_profile, self).render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = super(account_profile, self).get_context_data(**kwargs)
        usuario = request.user
        usuario.first_name = request.POST.get('first_name')
        usuario.last_name = request.POST.get('last_name')
        usuario.email = request.POST.get('email')
        usuario.profile.telefono = request.POST.get('telefono')

        if usuario.check_password(request.POST.get('password')):
            usuario.set_password(request.POST.get('new_password'))

        context["success_message"] = "Datos actualizados"
        return super(account_profile, self).render_to_response(context)


class negocio_form(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    direccion = forms.CharField(label='Direcion', max_length=500,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefono = forms.CharField(label='Telefono', max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    identificacion = forms.CharField(label='RUC/NIT', max_length=50,
                                     widget=forms.TextInput(attrs={'class': 'form-control'}))
    categoria = forms.ModelChoiceField(queryset=Comercio_Categoria.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    logo = forms.ImageField()

    def save(self, user, commit=True):
        categoria = self.cleaned_data['categoria']
        comercio = Comercio.objects.filter(propietario=user).first()
        if not comercio:
            comercio, create = Comercio.objects.get_or_create(identificacion=self.cleaned_data['identificacion'],
                                                              propietario=user)

        comercio.nombre = self.cleaned_data['nombre']
        comercio.telefono = self.cleaned_data['telefono']
        comercio.categoria = categoria
        comercio.logo = self.cleaned_data['logo']
        comercio.direccion = self.cleaned_data['direccion']
        if commit:
            comercio.save()
        return comercio


class registrar_negocio(TemplateView):
    template_name = "arca/registrar_negocio.html"

    def get(self, request, *args, **kwargs):
        context = super(registrar_negocio, self).get_context_data(**kwargs)
        context["form"] = negocio_form()
        return super(registrar_negocio, self).render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = super(registrar_negocio, self).get_context_data(**kwargs)
        form = negocio_form(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            comercio = form.save(commit=False, user=request.user)
            comercio.propietario = request.user
            comercio.save()
            context["form"] = form
            context["success_message"] = "Datos actualizados exitosamente!"
            return redirect("mi_comercio")
        else:
            context["form"] = form

        return super(registrar_negocio, self).render_to_response(context)


class mi_comercio(TemplateView):
    template_name = "arca/mi_empresa.html"

    def get(self, request, *args, **kwargs):
        context = super(mi_comercio, self).get_context_data(**kwargs)
        return super(mi_comercio, self).render_to_response(context)


def render_descuento(request):
    id = request.GET.get('id')
    if id:
        descuento = Descuento.objects.filter(id=id).first()
    else:
        descuento = Descuento()

    descuento.comercio = request.user.profile.comercio()
    html = render_to_string('arca/_descuento.html',
                            {'descuento': descuento})
    return HttpResponse(html)


def render_listado_descuento(request):
    descuentos = Descuento.objects.filter(comercio=request.user.profile.comercio()).order_by('-activo')
    html = render_to_string('arca/_descuentos.html', {'descuentos': descuentos})
    return HttpResponse(html)


@csrf_exempt
def save_descuento(request):
    data = []
    obj_json = {}
    nombre = request.POST.get('nombre')
    porcentaje = request.POST.get('porcentaje')
    vigencia = request.POST.get('vigencia')
    id = request.POST.get('id')
    comercio = request.user.profile.comercio()

    if not comercio:
        obj_json['code'] = 400
        obj_json['mensaje'] = "Comercio invalido"
    elif not nombre:
        obj_json['code'] = 400
        obj_json['mensaje'] = "Nombre invalido"
    else:
        if id:
            descuento = Descuento.objects.filter(id=id).first()
        else:
            descuento, create = Descuento.objects.get_or_create(
                comercio=comercio,
                nombre=nombre,
                porcentaje_descuento=porcentaje,
                vigencia=vigencia,
                creado_por=request.user
            )

        descuento.save()
        obj_json['code'] = 200
        obj_json['mensaje'] = "Descuento registrado exitosamente!"

    data.append(obj_json)
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')
