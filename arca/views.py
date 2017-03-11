from django.shortcuts import render
from .models import *
import json

from django import forms

from arca.models import *
from django.forms import ModelForm
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from social_django import *
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
from django.views.generic import TemplateView
from social_django.models import UserSocialAuth

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

class login_comercio(TemplateView):
    template_name = "arca/comercio/login_comercio.html"

    def get(self, request, *args, **kwargs):
        context = super(login_comercio, self).get_context_data(**kwargs)
        return super(login_comercio, self).render_to_response(context)

    def post(self, request, *args, **kwargs):
       comercio = None

       if request.method == "POST":
          username = request.POST.get('username', '')
          password = request.POST.get('password', '')
          comercio = autenticate(Comercio(), username, password)

       response = render(request, 'arca/comercio/login_comercio.html', {"comercio" : comercio})
       if comercio:
          response.set_cookie('comercio', comercio)

       return response


def index_comercio(request):
   if 'comercio' in request.COOKIES:
      comercio = request.COOKIES['comercio']

      response = render(request, 'arca2/app.html', {"comercio" : comercio})

   else:
      response = render(request, 'arca2/comercio.html', {})

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


class negocio_form(ModelForm):
    nombre = forms.CharField(label='Nombre', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    direccion = forms.CharField(label='Direcion', max_length=500,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefono = forms.CharField(label='Telefono', max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    identificacion = forms.CharField(label='RUC/NIT', max_length=50,
                                     widget=forms.TextInput(attrs={'class': 'form-control'}))
    categoria = forms.ModelChoiceField(queryset=Comercio_Categoria.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    logo = forms.ImageField(required=False)

    class Meta:
        model = Comercio
        fields = ['nombre', 'direccion', 'telefono', 'identificacion', 'categoria', 'logo']

    def save(self, user, commit=True):
        categoria = self.cleaned_data['categoria']
        comercio = Comercio.objects.filter(propietario=user).first()
        if not comercio:
            comercio, create = Comercio.objects.get_or_create(identificacion=self.cleaned_data['identificacion'],
                                                              propietario=user)

        comercio.nombre = self.cleaned_data['nombre']
        comercio.telefono = self.cleaned_data['telefono']
        comercio.categoria = categoria
        if self.cleaned_data['logo']:
            comercio.logo = self.cleaned_data['logo']
        comercio.direccion = self.cleaned_data['direccion']
        if commit:
            comercio.save()
        return comercio





class registrar_negocio_st1(TemplateView):
    template_name = "arca/comercio/registrar_negocio_st1.html"

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        context = super(registrar_negocio_st1, self).get_context_data(**kwargs)

        return super(registrar_negocio_st1, self).render_to_response(context)

    @csrf_exempt
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

class registrar_negocio_st2(TemplateView):
    template_name = "arca/comercio/registrar_negocio_st2.html"

    def get(self, request, *args, **kwargs):
        context = super(registrar_negocio_st2, self).get_context_data(**kwargs)
        return super(registrar_negocio_st2, self).render_to_response(context)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        context = super(registrar_negocio_st2, self).get_context_data(**kwargs)
        if not request.POST.get('nombre_empresa'):
            super(registrar_negocio_st1, self).render_to_response(context)
        else:
            request.session['nombre_empresa'] = request.POST.get('nombre_empresa')
            return super(registrar_negocio_st2, self).render_to_response(context)

class registrar_negocio_st3(TemplateView):
    template_name = "arca/comercio/registrar_negocio_st3.html"

    def get(self, request, *args, **kwargs):
        context = super(registrar_negocio_st3, self).get_context_data(**kwargs)
        return super(registrar_negocio_st3, self).render_to_response(context)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        context = super(registrar_negocio_st3, self).get_context_data(**kwargs)
        if not request.POST.get('identificacion'):
            super(registrar_negocio_st2, self).render_to_response(context)
        elif not request.POST.get('telefono'):
            super(registrar_negocio_st2, self).render_to_response(context)
        elif not request.POST.get('direccion'):
            super(registrar_negocio_st2, self).render_to_response(context)
        else:
            request.session['identificacion_empresa'] = request.POST.get('identificacion')
            request.session['telefono_empresa'] = request.POST.get('telefono')
            request.session['direccion_empresa'] = request.POST.get('direccion')
            return super(registrar_negocio_st3, self).render_to_response(context)

class registrar_negocio_st4(TemplateView):
    template_name = "arca/comercio/registrar_negocio_st4.html"

    def get(self, request, *args, **kwargs):
        context = super(registrar_negocio_st4, self).get_context_data(**kwargs)
        return super(registrar_negocio_st4, self).render_to_response(context)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        context = super(registrar_negocio_st4, self).get_context_data(**kwargs)
        if not request.POST.get('usuario_nombre'):
            super(registrar_negocio_st3, self).render_to_response(context)
        elif not request.POST.get('usuario_apellido'):
            super(registrar_negocio_st3, self).render_to_response(context)
        elif not request.POST.get('email'):
            super(registrar_negocio_st3, self).render_to_response(context)
        elif not request.POST.get('password'):
            super(registrar_negocio_st3, self).render_to_response(context)
        else:
            request.session['usuario_nombre'] = request.POST.get('usuario_nombre')
            request.session['usuario_apellido'] = request.POST.get('usuario_apellido')
            request.session['usuario_email'] = request.POST.get('email')
            request.session['usuario_password'] = request.POST.get('password')
            return super(registrar_negocio_st4, self).render_to_response(context)

class registrar_negocio(TemplateView):
    template_name = "arca/comercio/registrar_negocio.html"

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        context = super(registrar_negocio, self).get_context_data(**kwargs)
        nombre_empresa = request.session['nombre_empresa']
        identificacion_empresa = request.session['identificacion_empresa']
        direccion_empresa = request.session['direccion_empresa']
        telefono_empresa = request.session['telefono_empresa']
        usuario_nombre = request.session['usuario_nombre']
        usuario_apellido = request.session['usuario_apellido']
        usuario_email = request.session['usuario_email']
        usuario_password = request.session['usuario_password']

        comercio, create = Comercio.objects.get_or_create(identificacion=identificacion_empresa)
        comercio.nombre=nombre_empresa
        comercio.direccion=direccion_empresa
        comercio.telefono=telefono_empresa
        comercio.username=usuario_email
        comercio.password=usuario_password
        comercio.nombre=usuario_nombre + " " + usuario_apellido
        comercio.save()

        comercio = autenticate(Comercio(), usuario_email, usuario_password)

        response = render(request, 'arca/mi_empresa.html', {"comercio": comercio})
        if comercio:
            response.set_cookie('comercio', comercio.id)

        return response

class mi_comercio(TemplateView):
    template_name = "arca/mi_empresa.html"

    def get(self, request, *args, **kwargs):
        context = super(mi_comercio, self).get_context_data(**kwargs)

        if 'comercio' in request.COOKIES:
            comercio = Comercio.objects.get(id=int(request.COOKIES['comercio']))
            context['comercio']=comercio
            context['empleados'] = comercio.usuarios_empleados()
        return super(mi_comercio, self).render_to_response(context)


def render_descuento(request):
    id = request.GET.get('id')
    if id:
        descuento = Descuento.objects.filter(id=id).first()
    else:
        descuento = Descuento()

    descuento.comercio = request.user.perfil.comercio()
    html = render_to_string('arca/_descuento.html',
                            {'descuento': descuento})
    return HttpResponse(html)


def render_listado_descuento(request):
    comercio = None
    if 'comercio' in request.COOKIES:
        comercio = Comercio.objects.get(id=int(request.COOKIES['comercio']))
    descuentos = Descuento.objects.filter(comercio=comercio).order_by('-activo')

    html = render_to_string('arca/_descuentos.html', {'descuentos': descuentos,'comercio':comercio})
    return HttpResponse(html)


@csrf_exempt
def save_descuento(request):
    data = []
    obj_json = {}
    nombre = request.POST.get('nombre')
    porcentaje = request.POST.get('porcentaje')
    vigencia = request.POST.get('vigencia')

    vigencia_param = request.POST.get('vigencia_param')
    vigencia_porc_inf = request.POST.get('vigencia_porc_inf')
    vigencia_porc_sup = request.POST.get('vigencia_porc_sup')

    compra_min_param = request.POST.get('compra_min_param')
    compra_minima_porc_inf = request.POST.get('compra_minima_porc_inf')
    compra_minima_porc_sup = request.POST.get('compra_minima_porc_sup')

    id = request.POST.get('id')
    comercio = request.user.perfil.comercio()

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
        descuento.nombre = nombre
        descuento.porcentaje_descuento = porcentaje
        descuento.vigencia = vigencia

        if vigencia_param:
            descuento.desc_dia_vigencia = vigencia_param
            descuento.desc_dia_vigencia_porc_inf = vigencia_porc_inf
            descuento.desc_dia_vigencia_porc_sup = vigencia_porc_sup
        else:
            descuento.desc_dia_vigencia = None
            descuento.desc_dia_vigencia_porc_inf = None
            descuento.desc_dia_vigencia_porc_sup = None

        if compra_min_param:
            descuento.desc_compra_minima = compra_min_param
            descuento.desc_compra_minima_porc_inf = compra_minima_porc_inf
            descuento.desc_compra_minima_porc_sup = compra_minima_porc_sup
        else:
            descuento.desc_compra_minima = None
            descuento.desc_compra_minima_porc_inf = None
            descuento.desc_compra_minima_porc_sup = None

        descuento.save()
        obj_json['code'] = 200
        obj_json['mensaje'] = "Descuento registrado exitosamente!"

    data.append(obj_json)
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')


def render_listado_cupones(request):
    comercio = None
    if 'comercio' in request.COOKIES:
        comercio = Comercio.objects.get(id=int(request.COOKIES['comercio']))
    descuentos = Descuento.objects.filter(comercio=comercio).order_by('-activo')

    cupones = Codigo_Descuento.objects.filter(descuento__in=descuentos)

    page = request.GET.get('page', 1)

    for k, vals in request.GET.lists():
        for v in vals:
            if not k == 'page' and not k == '_':
                cupones = cupones.filter(**{k: v})

    paginator = Paginator(cupones, 3)
    try:
        cupones = paginator.page(page)
    except PageNotAnInteger:
        cupones = paginator.page(1)
    except EmptyPage:
        cupones = paginator.page(paginator.num_pages)

    html = render_to_string('arca/_cupones.html', {'cupones': cupones})
    return HttpResponse(html)


def render_cupon(request):
    id = request.GET.get('id')
    if id:
        cupon = Codigo_Descuento.objects.filter(id=id).first()
    else:
        cupon = Codigo_Descuento()
    descuentos = Descuento.objects.filter(comercio=request.user.perfil.comercio(), activo=True)
    html = render_to_string('arca/_cupon.html',
                            {'cupon': cupon, 'descuentos': descuentos})
    return HttpResponse(html)


@csrf_exempt
def save_cupon(request):
    data = []
    obj_json = {}
    id_descuento = request.POST.get('descuento')
    codigo = request.POST.get('codigo')

    id = request.POST.get('id')
    comercio = request.user.perfil.comercio()
    usuario = request.user
    if not usuario:
        obj_json['code'] = 400
        obj_json['mensaje'] = "Usuario invalido"
    if not codigo:
        obj_json['code'] = 400
        obj_json['mensaje'] = "Codigo invalido"
    elif not id_descuento:
        obj_json['code'] = 400
        obj_json['mensaje'] = "Descuento invalido"
    else:
        descuento = Descuento.objects.filter(id=id_descuento).first()
        if not descuento:
            obj_json['code'] = 400
            obj_json['mensaje'] = "Descuento no encontrado"
        else:
            if id:
                cupon = Codigo_Descuento.objects.filter(codigo=codigo).first()
                cupon.descuento = descuento
                cupon.save()
            else:
                cupon, create = Codigo_Descuento.objects.get_or_create(codigo=codigo, descuento=descuento,
                                                                       creado_por=usuario)

            obj_json['code'] = 200
            obj_json['mensaje'] = "Descuento registrado exitosamente!"

    data.append(obj_json)
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')

