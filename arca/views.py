# coding=utf-8
from django.urls import reverse

from arca.crypter import encrypt_val
from django.template import Context
import json

from django import forms
from django.core import serializers
from arca.models import *
from django.forms import ModelForm
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
from django.views.generic import TemplateView


def login_app(request):
    usuario = None

    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        usuario = autenticate(Usuario(), username, password)

    response = render(request, 'arca2/app.html', {"usuario": usuario})
    if usuario:
        response.set_cookie('auth_usuario', usuario.id)

    return response


def index_app(request):
    c = Context()
    c = authorize(request, c)
    response = render(request, 'arca2/app.html', c)
    return response


class login_comercio(TemplateView):
    template_name = "arca/comercio/login_comercio.html"

    def get(self, request, *args, **kwargs):
        context = super(login_comercio, self).get_context_data(**kwargs)
        return super(login_comercio, self).render_to_response(context)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('email', '')
        password = request.POST.get('password', '')
        es_comercio = request.POST.get('ckcomercio', False)
        if es_comercio:
            comercio = autenticate(Comercio(), username, password)
            if comercio:
                response = HttpResponseRedirect("/arca/mi_comercio")
                response.set_cookie('auth_comercio', encrypt_val(comercio.id))
                return response
            else:
                context = super(login_comercio, self).get_context_data(**kwargs)
                context['email'] = username
                context['password'] = password
                context['ckcomercio'] = es_comercio
                context['error_message'] = "Usuario o contraseña invalido"

                return super(login_comercio, self).render_to_response(context)
        else:
            empleado = autenticate(Empleado(), username, password)
            if empleado:
                response = HttpResponseRedirect("/arca/dashboard_comercio")
                response.set_cookie('auth_empleado', encrypt_val(empleado.id))
                return response
            else:
                context = super(login_comercio, self).get_context_data(**kwargs)
                context['email'] = username
                context['password'] = password
                context['ckcomercio'] = es_comercio
                context['error_message'] = "Usuario o contraseña invalido"

                return super(login_comercio, self).render_to_response(context)


def logout_comercio(request):
    response = HttpResponseRedirect("/arca/login_comercio")
    try:
        if 'auth_comercio' in request.COOKIES:
            response.delete_cookie('auth_comercio')
    except:
        pass
    try:
        if 'auth_empleado' in request.COOKIES:
            response.delete_cookie('auth_empleado')
    except:
        pass
    return response


def index_comercio(request):
    if 'comercio' in request.COOKIES:
        comercio = request.COOKIES['comercio']
        response = render(request, 'arca2/app.html', {"comercio": comercio})
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
    template_name = "arca/indexnew.html"

    def get(self, request, *args, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context = authorize(request, context)
        context['categorias'] = Comercio_Categoria.objects.all().order_by('nombre')
        return super(Index, self).render_to_response(context)


def get_comercio_categorias(request):
    categorias = Comercio_Categoria.objects.all()
    data = []
    for categoria in categorias:
        obj_json = {}
        obj_json['id'] = categoria.id
        obj_json['nombre'] = categoria.nombre
        obj_json['icono'] = str(categoria.icono)
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


# region USUARIO
@csrf_exempt
def createUserAuth(request):
    obj_json = {}
    username = request.POST.get("username")
    nombre = request.POST.get("nombre")
    apellido = request.POST.get("apellido")
    age = request.POST.get("age", "0")
    gender = request.POST.get("gender", None)
    email = request.POST.get("email", None)
    telefono = request.POST.get("telefono", None)
    if age == "null":
        age = 0
    if telefono == "null":
        telefono = None
    if gender == "null":
        gender = None

    if not username:
        obj_json['code'] = 400
        obj_json['mensaje'] = "No es posible autenticar al usuario"
    else:
        usuario = Usuario.objects.filter(username=username).first()
        if usuario:
            usuario.nombre = nombre
            usuario.apellido = apellido
            if int(age) > 0:
                usuario.age = int(age)
            if gender:
                usuario.gender = gender
            usuario.email = email
            if telefono:
                usuario.telefono = telefono
        else:
            usuario, create = Usuario.objects.get_or_create(username=username)
            usuario.nombre = nombre
            usuario.apellido = apellido
            usuario.age = int(age)
            usuario.gender = gender
            usuario.email = email
            usuario.telefono = telefono
        usuario.save()
        obj_json['codigo'] = str(usuario.codigo)
        obj_json['id_usuario'] = usuario.id
        obj_json['age'] = usuario.age
        obj_json['gender'] = usuario.gender
        obj_json['telefono'] = usuario.telefono
        obj_json['code'] = 200

    data = json.dumps(obj_json)
    return HttpResponse(data, content_type='application/json')


# endregion
# region COMERCIO ADMIN
class negocio_form(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    password_new = forms.CharField(label='Nueva Contraseña', max_length=100, required=False,
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password_conf = forms.CharField(label='Confirmar Contraseña', max_length=100, required=False,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Comercio
        fields = ['nombre', 'direccion', 'telefono', 'identificacion',
                  'categoria', 'logo', 'username', 'password', 'position']

    def __init__(self, *args, **kwargs):
        super(negocio_form, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    def clean(self):
        cleaned_data = super(negocio_form, self).clean()
        new_password = cleaned_data.get("password_new")
        confirm_password = cleaned_data.get("password_conf")

        if new_password != confirm_password:
            # raise forms.ValidationError("password and confirm_password does not match")
            self.add_error("password_new", "Nueva contraseña y contraseña de confirmacion no coinsiden")

    def save(self, commit=True):
        categoria = self.cleaned_data['categoria']
        comercio = Comercio.objects.filter(identificacion=self.cleaned_data['identificacion']).first()
        if not comercio:
            comercio, create = Comercio.objects.get_or_create(identificacion=self.cleaned_data['identificacion'])

        comercio.nombre = self.cleaned_data['nombre']
        comercio.telefono = self.cleaned_data['telefono']
        comercio.categoria = categoria
        if self.cleaned_data['logo']:
            comercio.logo = self.cleaned_data['logo']
        if encrypt_val(self.cleaned_data['password']) == comercio.password:
            if len(self.cleaned_data['password_new']) > 0:
                comercio.password = encrypt_val(self.cleaned_data['password_new'])
        comercio.direccion = self.cleaned_data['direccion']
        if commit:
            comercio.save()
        return comercio


class mi_comercio(TemplateView):
    template_name = "arca/comercio/mi_comercio.html"

    def get(self, request, *args, **kwargs):
        context = super(mi_comercio, self).get_context_data(**kwargs)
        context = authorize(request, context)
        if context.get('auth_comercio'):
            comercio = context.get('auth_comercio')
            context['empleados'] = comercio.empleados()
            return super(mi_comercio, self).render_to_response(context)
        else:
            return HttpResponseRedirect("/arca/login_comercio")

            # @csrf_exempt
            # def post(self, request, *args, **kwargs):
            #    return HttpResponseRedirect("/arca/login_comercio")


class edit_comercio(TemplateView):
    template_name = "arca/comercio/registrar_negocio.html"

        # check whether it's valid:
    @csrf_exempt
    def get(self, request, *args, **kwargs):

        context = super(edit_comercio, self).get_context_data(**kwargs)
        context = authorize(request, context)

        if context.get('auth_comercio'):
            comercio = context.get('auth_comercio')
            if comercio:
                comercio_form = negocio_form(instance=comercio)
            else:
                comercio_form = negocio_form()
            context["form"] = comercio_form
            return super(edit_comercio, self).render_to_response(context)
        else:
            return HttpResponseRedirect("/arca/login_comercio")

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        context = super(edit_comercio, self).get_context_data(**kwargs)
        form = negocio_form(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            comercio = form.save(commit=True)
            context["form"] = form
            context["success_message"] = "Datos actualizados exitosamente!"
            return redirect("mi_comercio")
        else:
            context["form"] = form

        return super(edit_comercio, self).render_to_response(context)

@csrf_exempt
def get_comercios(request):
    comercios = Comercio.objects.all()
    jcomercios = []
    for comercio in comercios:
        jcomercio = {'id': comercio.id, 'nombre': comercio.nombre, 'direccion': comercio.direccion,
                     'telefono': comercio.telefono, 'rating': comercio.rating()}

        if comercio.position:
            jcomercio['latitude'] = float(comercio.position.latitude)
            jcomercio['longitude'] = float(comercio.position.longitude)

        if comercio.logo:
            jcomercio['logo'] = comercio.logo.url

        if comercio.baner:
            jcomercio['baner'] = comercio.baner.url

        if comercio.categoria:
            jcomercio['categoria'] = {
                'id': comercio.categoria.id,
                'nombre': comercio.categoria.nombre,
                'icono': str(comercio.categoria.icono)}
        else:
            jcomercio['categoria'] = {
                'id': 0,
                'nombre': 'Sin categoria'}

        jdescuentos = []
        for descuento in comercio.descuentos():
            jdescuento = {
                'id': descuento.id,
                'nombre': descuento.nombre,
                'porcentaje_descuento': descuento.porcentaje_descuento,
                'vigencia': descuento.vigencia,
                'desc_dia_vigencia': descuento.desc_dia_vigencia,
                'desc_dia_vigencia_porc_inf': descuento.desc_dia_vigencia_porc_inf,
                'desc_dia_vigencia_porc_sup': descuento.desc_dia_vigencia_porc_sup,
                'desc_compra_minima': descuento.desc_compra_minima,
                'desc_compra_minima_porc_inf': descuento.desc_compra_minima_porc_inf,
                'desc_compra_minima_porc_sup': descuento.desc_compra_minima_porc_sup,
                'tipo_cambio': descuento.tipo_cambio,
                'activo': descuento.activo
            }
            jdescuentos.append(jdescuento)
        jcomercio['descuentos'] = jdescuentos
        jproductos = []
        for producto in comercio.productos():
            tmp_producto = {
                'id': producto.id,
                'nombre': producto.nombre,
                'descripcion': producto.descripcion,
                'precio': producto.precio,
                'descuento': producto.descuento,
                'activo': producto.activo
            }
            if producto.imagen:
                tmp_producto['imagen'] = producto.imagen.url
            else:
                tmp_producto['imagen'] = None

            jproductos.append(tmp_producto)
        jcomercio['productos'] = jproductos
        jcomercios.append(jcomercio)
    data = json.dumps(jcomercios)
    return HttpResponse(data, content_type='application/json')


# region REGISTRO DEL COMERCIO
class registrar_negocio_st1(TemplateView):
    template_name = "arca/comercio/registrar_negocio_st1.html"

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        context = super(registrar_negocio_st1, self).get_context_data(**kwargs)
        if request.session['categoria_empresa']:
            context['categoriaactual'] = int(request.session['categoria_empresa'])
        context['categorias'] = Comercio_Categoria.objects.all()
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
        elif not request.POST.get('categoria_empresa', None):
            super(registrar_negocio_st1, self).render_to_response(context)
        else:
            request.session['categoria_empresa'] = request.POST.get('categoria_empresa', None)
            request.session['nombre_empresa'] = request.POST.get('nombre_empresa', None)
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
        if request.session['categoria_empresa']:
            context['categoria'] = Comercio_Categoria.objects.filter(
                id=int(request.session['categoria_empresa'])).first()

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

        if Comercio.objects.filter(username=usuario_email).exists():
            context["error_message"] = "Ya existe un comercio registrado con esa dirección de correo electronico"

            categoria = None
            if request.session['categoria_empresa']:
                categoria = Comercio_Categoria.objects.filter(
                    id=int(request.session['categoria_empresa'])).first()

            html = render_to_string('arca/comercio/registrar_negocio_st4.html', context)
            return HttpResponse(html)

            # , kwargs={'error_message':
            #                                                      "Ya existe un comercio registrado con esa dirección de correo electronico"})
            # return redirect(registrar_negocio_st4())
        else:

            categoria = Comercio_Categoria.objects.filter(id=request.session['categoria_empresa']).first()

            comercio, create = Comercio.objects.get_or_create(identificacion=identificacion_empresa)
            comercio.nombre = nombre_empresa
            comercio.direccion = direccion_empresa
            comercio.telefono = telefono_empresa
            comercio.username = usuario_email
            comercio.password = encrypt_val(usuario_password)
            comercio.nombre_propietario = usuario_nombre + " " + usuario_apellido
            comercio.categoria = categoria
            comercio.save()

            comercio = autenticate(Comercio(), usuario_email, usuario_password)

            response = render(request, 'arca/comercio/mi_comercio.html', {"comercio": comercio})
            if comercio:
                response.set_cookie('auth_comercio', encrypt_val(comercio.id))

            return response


# endregion

# endregion
# region DESCUENTOS
def render_descuento(request):
    id = request.GET.get('id')
    if id:
        descuento = Descuento.objects.filter(id=id).first()
    else:
        descuento = Descuento()

    context = Context()
    context = authorize(request, context)
    if context.get('auth_comercio'):
        comercio = context.get('auth_comercio')
        descuento.comercio = comercio

        html = render_to_string('arca/comercio/_descuento.html',
                                {'descuento': descuento})
        return HttpResponse(html)


def render_listado_descuento(request):
    context = Context()
    context = authorize(request, context)
    if context.get('auth_comercio'):
        comercio = context.get('auth_comercio')
        descuentos = Descuento.objects.filter(comercio=comercio).order_by('-activo', '-actualizado')
        context['descuentos'] = descuentos
        html = render_to_string('arca/comercio/_descuentos.html', context)
        return HttpResponse(html)


@csrf_exempt
def save_descuento(request):
    data = []
    obj_json = {}
    nombre = request.POST.get('nombre')
    porcentaje = request.POST.get('porcentaje')
    vigencia = request.POST.get('vigencia')
    activo = request.POST.get('activo')
    if activo == 'on':
        activo = True
    else:
        activo = False

    vigencia_param = request.POST.get('vigencia_param')
    vigencia_porc_inf = request.POST.get('vigencia_porc_inf')
    vigencia_porc_sup = request.POST.get('vigencia_porc_sup')

    compra_min_param = request.POST.get('compra_min_param')
    compra_minima_porc_inf = request.POST.get('compra_minima_porc_inf')
    compra_minima_porc_sup = request.POST.get('compra_minima_porc_sup')

    id = request.POST.get('id')
    context = Context()
    context = authorize(request, context)
    if context.get('auth_comercio'):
        comercio = context.get('auth_comercio')

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
                vigencia=vigencia
            )
        descuento.nombre = nombre
        descuento.porcentaje_descuento = porcentaje
        descuento.vigencia = vigencia
        descuento.activo = activo

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


def get_descuentos(request):
    obj_json = {}
    id_comercio = request.GET.get("id_comercio")
    if not id_comercio:
        obj_json['code'] = 400
        obj_json['mensaje'] = "Comercio invalido"
    else:
        comercio = Comercio.objects.filter(id=id_comercio).first()
        if not comercio:
            obj_json['code'] = 400
            obj_json['mensaje'] = "Comercio no encontrado"
        else:
            descuentos = Descuento.objects.filter(comercio=comercio)
            obj_descuentos = []
            for descuento in descuentos:
                obj_descuento = {
                    'id': descuento.id,
                    'nombre': descuento.nombre,
                    'porcentaje_descuento': descuento.porcentaje_descuento,
                    'vigencia': descuento.vigencia,
                    'desc_dia_vigencia': descuento.desc_dia_vigencia,
                    'desc_dia_vigencia_porc_inf': descuento.desc_dia_vigencia_porc_inf,
                    'desc_dia_vigencia_porc_sup': descuento.desc_dia_vigencia_porc_sup,
                    'desc_compra_minima': descuento.desc_compra_minima,
                    'desc_compra_minima_porc_inf': descuento.desc_compra_minima_porc_inf,
                    'desc_compra_minima_porc_sup': descuento.desc_compra_minima_porc_sup
                }
                obj_descuentos.append(obj_descuento)
            obj_json['code'] = 200
            obj_json['mensaje'] = "OK"
            obj_json['descuentos'] = obj_descuentos

    data = json.dumps(obj_json)
    return HttpResponse(data, content_type='application/json')


# endregion
# region CUPONES
def get_cupones(request):
    obj_json = {}
    username = request.GET.get("username")
    usuario = Usuario.objects.filter(username=username).first()
    obj_cupnes = []
    if usuario:
        cupones = usuario.cupones()
        for cupon in cupones:
            obj_cupon = {
                'id': cupon.id,
                'codigo': cupon.codigo,
                'canjeado': cupon.canjeado,
                'creado': str(cupon.creado),
                'actualizado': str(cupon.actualizado),
                'creado_por': {
                    'id': cupon.creado_por.id,
                    'nombre': "%s %s" % (cupon.creado_por.nombre, cupon.creado_por.apellido)
                },
                'id_descuento': cupon.descuento.id,
            }

            if cupon.actualizado_por:
                obj_cupon['actualizado_por'] = {
                                                   'id': cupon.actualizado_por.id,
                                                   'nombre': "%s %s" % (
                                                       cupon.actualizado_por.nombre, cupon.actualizado_por.apellido)
                                               },
            obj_cupnes.append(obj_cupon)
        obj_json['cupones'] = obj_cupnes
        obj_json['code'] = 200
    else:
        obj_json['mensaje'] = "Usuario invalido"
        obj_json['code'] = 400

    data = json.dumps(obj_json)
    return HttpResponse(data, content_type='application/json')


def get_facturas(request):
    obj_json = {}
    username = request.GET.get("username")
    usuario = Usuario.objects.filter(username=username).first()
    obj_detalle = []
    if usuario:
        facturas = usuario.facturas()
        for factura in facturas:
            obj_detalle.append({
                'id': factura.id,
                'documento': factura.documento,
                'comercio_id': factura.comercio.id,
                'monto': factura.monto,
                'descuento': factura.descuento,
                'cupon_id': factura.cupon.id,
                'fecha': str(factura.fecha),
            })
        obj_json['facturas'] = obj_detalle
        obj_json['code'] = 200
    else:
        obj_json['mensaje'] = "Empleado invalido"
        obj_json['code'] = 400

    data = json.dumps(obj_json)
    return HttpResponse(data, content_type='application/json')


def get_cupones_empleado(request):
    obj_json = {}
    id_empleado = request.GET.get("id_empleado")
    empleado = Empleado.objects.filter(id=id_empleado).first()
    obj_cupnes = []
    if empleado:
        cupones = empleado.codigos_descuento()
        for cupon in cupones:
            obj_cupon = {
                'id': cupon.id,
                'codigo': cupon.codigo,
                'canjeado': cupon.canjeado,
                'creado': str(cupon.creado),
                'actualizado': str(cupon.actualizado),
                'creado_por': {
                    'id': cupon.creado_por.id,
                    'nombre': "%s %s" % (cupon.creado_por.nombre, cupon.creado_por.apellido)
                },
                'id_descuento': cupon.descuento.id,
            }

            if cupon.actualizado_por:
                obj_cupon['actualizado_por'] = {
                                                   'id': cupon.actualizado_por.id,
                                                   'nombre': "%s %s" % (
                                                       cupon.actualizado_por.nombre, cupon.actualizado_por.apellido)
                                               },
            obj_cupnes.append(obj_cupon)
        obj_json['cupones'] = obj_cupnes
        obj_json['code'] = 200
    else:
        obj_json['mensaje'] = "Empleado invalido"
        obj_json['code'] = 400

    data = json.dumps(obj_json)
    return HttpResponse(data, content_type='application/json')


def get_facturas_empleado(request):
    obj_json = {}
    id_empleado = request.GET.get("id_empleado")
    empleado = Empleado.objects.filter(id=id_empleado).first()
    obj_detalle = []
    if empleado:
        facturas = empleado.facturas()
        for factura in facturas:
            obj_detalle.append({
                'id': factura.id,
                'documento': factura.documento,
                'comercio_id': factura.comercio.id,
                'monto': factura.monto,
                'descuento': factura.descuento,
                'cupon_id': factura.cupon.id,
                'fecha': str(factura.fecha),
            })
        obj_json['facturas'] = obj_detalle
        obj_json['code'] = 200
    else:
        obj_json['mensaje'] = "Empleado invalido"
        obj_json['code'] = 400

    data = json.dumps(obj_json)
    return HttpResponse(data, content_type='application/json')


def render_listado_cupones(request):
    context = Context()
    context = authorize(request, context)
    if context.get('auth_comercio'):
        comercio = context.get('auth_comercio')
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

        html = render_to_string('arca/comercio/_cupones.html', {'cupones': cupones})
        return HttpResponse(html)


def render_cupon(request):
    id = request.GET.get('id')
    if id:
        cupon = Codigo_Descuento.objects.filter(id=id).first()
    else:
        cupon = Codigo_Descuento()

    context = Context()
    context = authorize(request, context)
    if context.get('auth_comercio'):
        comercio = context.get('auth_comercio')
    elif context.get('aut_empleado'):
        comercio = context.get('auth_empleado').comercio

    descuentos = Descuento.objects.filter(comercio=comercio, activo=True)
    html = render_to_string('arca/comercio/_cupon.html',
                            {'cupon': cupon, 'descuentos': descuentos})
    return HttpResponse(html)


@csrf_exempt
def save_cupon(request):
    context = Context()
    context = authorize(request, context)
    obj_json = {}
    id_descuento = request.POST.get('descuento')
    id_empleado = request.POST.get('id_empleado')
    codigo_usurio = request.POST.get('codigo_usuario')
    codigo = request.POST.get('codigo')
    creado = request.POST.get('creado', '')
    id = request.POST.get('id')

    if id_empleado:
        empleado = Empleado.objects.filter(id=id_empleado).first()

    usuario = None
    if codigo_usurio:
        usuario = Usuario.objects.filter(codigo=codigo_usurio).first()

    if not empleado:
        if context.get('aut_empleado'):
            empleado = context.get('auth_empleado')

    if not empleado:
        obj_json['code'] = 400
        obj_json['mensaje'] = "Empleado invalido"
    elif not usuario:
        obj_json['code'] = 400
        obj_json['mensaje'] = "Codigo de usuario invalido"
    elif not codigo:
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
                cupon.actualizado_por = empleado
                cupon.save()
                obj_json['code'] = 200
                obj_json['mensaje'] = "Descuento actualizado exitosamente!"
            else:
                if not creado:
                    obj_json['code'] = 400
                    obj_json['mensaje'] = "Fecha de creacion invalida"
                else:
                    cupon, create = Codigo_Descuento.objects.get_or_create(codigo=codigo,
                                                                           descuento=descuento,
                                                                           cliente=usuario,
                                                                           creado_por=empleado)
                    cupon.creado = creado
                    cupon.save()
                    obj_json['id_cupon'] = cupon.id
                    obj_json['code'] = 200
                    obj_json['mensaje'] = "Descuento registrado exitosamente!"

    data = json.dumps(obj_json)
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def canjear_cupon(request):
    obj_json = {}
    codigo_cupon = request.POST.get("codigo_cupon", None)
    numer_factura = request.POST.get("factura", None)
    monto = request.POST.get("monto", 0)
    descuento = request.POST.get("descuento", 0)
    actualizado = request.POST.get('actualizado', '')
    id_empleado = request.POST.get('id_empleado')

    if id_empleado:
        empleado = Empleado.objects.filter(id=id_empleado).first()

    cupon = Codigo_Descuento.objects.filter(codigo=codigo_cupon).first()

    if cupon.canjeado:
        obj_json['code'] = 400
        obj_json['mensaje'] = "Cupon ya fue canjeado"
    elif not empleado:
        obj_json['code'] = 400
        obj_json['mensaje'] = "Empleado invalido"
    elif not cupon:
        obj_json['code'] = 400
        obj_json['mensaje'] = "Cupon invalido"
    elif not numer_factura:
        obj_json['code'] = 400
        obj_json['mensaje'] = "Factura invalido"
    elif monto <= 0:
        obj_json['code'] = 400
        obj_json['mensaje'] = "Monto invalido"
    elif descuento <= 0 or descuento > monto:
        obj_json['code'] = 400
        obj_json['mensaje'] = "Descuento invalido"
    else:

        nuevo_cupon, c = Codigo_Descuento.objects.get_or_create(
            descuento=cupon.descuento,
            canjeado=False,
            cliente=cupon.cliente,
            creado_por=empleado
        )
        if not nuevo_cupon:
            obj_json['code'] = 500
            obj_json['mensaje'] = "No fue posible generar el nuvo cupon"
        else:
            factura, c = Factura.objects.get_or_create(
                cupon=cupon,
                comercio=cupon.descuento.comercio
            )
            factura.monto = monto
            factura.descuento = descuento
            factura.documento = numer_factura
            cupon.actualizado_por = empleado
            cupon.actualizado = actualizado
            cupon.cajeado = True
            cupon.save()
            factura.save()

            obj_json['code'] = 200
            obj_json['id_factura'] = factura.id
            obj_json['mensaje'] = "Descuento canjeado exitosamente"

    data = json.dumps(obj_json)
    return HttpResponse(data, content_type='application/json')


def generar_cupon(request):
    data = []
    obj_json = {}

    id_descuento = request.POST.get('descuento')
    id_empleado = request.POST.get('id_empleado')
    if id_empleado:
        empleado = Empleado.objects.filter(id=id_empleado).first()

    if not empleado:
        obj_json['code'] = 400
        obj_json['mensaje'] = "Empleado invalido"
    elif not id_descuento:
        obj_json['code'] = 400
        obj_json['mensaje'] = "Descuento invalido"
    else:
        descuento = Descuento.objects.filter(id=id_descuento).first()
        if not descuento:
            obj_json['code'] = 400
            obj_json['mensaje'] = "Descuento no encontrado"
        else:
            cupon, create = Codigo_Descuento.objects.get_or_create(descuento=descuento,
                                                                   creado_por=empleado)
            obj_json['codigo'] = cupon.codigo

    data = json.dumps(obj_json)
    return HttpResponse(data, content_type='application/json')


# endregion
# region EMPLEADO
def render_empleado(request):
    id = request.GET.get('id')
    if id:
        empleado = Empleado.objects.filter(id=id).first()
    else:
        empleado = Empleado()

    context = Context()
    context = authorize(request, context)
    if context.get('auth_comercio'):
        empleado.comercio = context.get('auth_comercio')
        context['empleado'] = empleado
        html = render_to_string('arca/comercio/_empleado.html', context)
        return HttpResponse(html)


def render_listado_empleado(request):
    context = Context()
    context = authorize(request, context)
    if context.get('auth_comercio'):
        comercio = context.get('auth_comercio')
        empleados = Empleado.objects.filter(comercio=comercio).order_by('-fecha_baja')
        context['empleados'] = empleados
        html = render_to_string('arca/comercio/_empleados.html', context)
        return HttpResponse(html)


@csrf_exempt
def save_empleado(request):
    data = []
    obj_json = {}
    nombre = request.POST.get('nombre')
    apellido = request.POST.get('apellido')
    direccion = request.POST.get('direccion')
    telefono = request.POST.get('telefono')
    username = request.POST.get('username')
    password = request.POST.get('password')
    password_conf = request.POST.get('password_conf')

    id = request.POST.get('id')
    context = Context()
    context = authorize(request, context)

    if not nombre:
        obj_json['code'] = 400
        obj_json['mensaje'] = "Nombre invalido"
    if not apellido:
        obj_json['code'] = 400
        obj_json['mensaje'] = "Apellido invalido"
    elif not username:
        obj_json['code'] = 400
        obj_json['mensaje'] = "Nombre de Usuario invalido"
    elif not context.get('auth_comercio'):
        obj_json['code'] = 400
        obj_json['mensaje'] = "Comercio invalido, intente iniciar sesion nuevamente"
    else:
        comercio = context.get('auth_comercio')

        if id:

            if password != password_conf:
                obj_json['code'] = 500
                obj_json['mensaje'] = "Contraseña y confirmacion no coinciden"
            else:
                empleado = Empleado.objects.filter(id=id).first()
                empleado.comercio = comercio
                empleado.nombre = nombre
                empleado.apellido = apellido
                empleado.direccion = direccion
                empleado.telefono = telefono
                if password:
                    empleado.password = encrypt_val(password)
                if not request.POST.get("ckactivo"):
                    empleado.fecha_baja = datetime.datetime.now()
                else:
                    empleado.fecha_baja = None
                empleado.save()
                obj_json['code'] = 200
                obj_json['mensaje'] = "Empleado actualizado exitosamente!"
        else:
            if not password:
                obj_json['code'] = 400
                obj_json['mensaje'] = "Contraseña es requerida"
            else:
                if password != password_conf:
                    obj_json['code'] = 500
                    obj_json['mensaje'] = "Contraseña y confirmacion no coinciden"
                else:
                    empleado = Empleado.objects.filter(username=username).first()
                    if empleado:
                        obj_json['code'] = 500
                        obj_json[
                            'mensaje'] = "Ya existe un empleado con ese nombre de usuario, " \
                                         "porfavor elija otro nombre de usuario"
                    else:
                        empleado, create = Empleado.objects.get_or_create(nombre=nombre,
                                                                          apellido=apellido,
                                                                          comercio=comercio,
                                                                          direccion=direccion,
                                                                          telefono=telefono,
                                                                          username=username,
                                                                          password=encrypt_val(password))

                        obj_json['code'] = 200
                        obj_json['mensaje'] = "Empleado registrado exitosamente!"

    data.append(obj_json)
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')

@csrf_exempt
def actualizar_empleado(request):
    data = []
    obj_json = {}
    id_empleado = request.POST.get('id')
    nombre = request.POST.get('nombre')
    apellido = request.POST.get('apellido')
    direccion = request.POST.get('direccion')
    telefono = request.POST.get('telefono')
    username = request.POST.get('username')
    password = request.POST.get('password')
    password_conf = request.POST.get('password_conf')


    if not nombre:
        obj_json['code'] = 400
        obj_json['mensaje'] = "Nombre invalido"
    if not apellido:
        obj_json['code'] = 400
        obj_json['mensaje'] = "Apellido invalido"
    elif not username:
        obj_json['code'] = 400
        obj_json['mensaje'] = "Nombre de Usuario invalido"
    else:

        if password != password_conf:
            obj_json['code'] = 500
            obj_json['mensaje'] = "Contraseña y confirmacion no coinciden"
        else:
            empleado = Empleado.objects.filter(id=id_empleado).first()
            empleado.nombre = nombre
            empleado.apellido = apellido
            empleado.direccion = direccion
            empleado.telefono = telefono
            if password:
                empleado.password = encrypt_val(password)
            empleado.save()
            obj_json['code'] = 200
            obj_json['mensaje'] = "Empleado actualizado exitosamente!"

    data.append(obj_json)
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')

def get_empleado(request):
    obj_json = {}
    username = request.GET.get("username", "")
    password = request.GET.get("password", "")
    empleado = autenticate(Empleado(), username, password)
    if not empleado:
        obj_json['code'] = 400
        obj_json['mensaje'] = "Empleado no encontrado"
    else:
        obj_empleado = {}
        obj_empleado["id"] = empleado.id
        obj_empleado["nombre"] = empleado.nombre
        obj_empleado["apellido"] = empleado.apellido
        obj_empleado["direccion"] = empleado.direccion
        obj_empleado["telefono"] = empleado.telefono
        obj_empleado["fecha_alta"] = str(empleado.fecha_alta)
        obj_empleado["fecha_baja"] = str(empleado.fecha_baja)

        obj_comercio = {}
        obj_comercio["id"] = empleado.comercio.id
        obj_comercio["nombre"] = empleado.comercio.nombre

        obj_empleado["comercio"] = obj_comercio

        obj_json['empleado'] = obj_empleado

        obj_json['code'] = 200
        obj_json['mensaje'] = "Empleado encontrado"

    data = json.dumps(obj_json)
    return HttpResponse(data, content_type='application/json')


def get_empleado_descuentos(request):
    obj_json = {}
    id_empleado = request.GET.get("id_empleado")

    if not id_empleado:
        obj_json['code'] = 400
        obj_json['mensaje'] = "Empleado no encontrado"
    else:
        empleado = Empleado.objects.filter(id=id_empleado).first()
        if not empleado:
            obj_json['code'] = 400
            obj_json['mensaje'] = "Empleado no encontrado"
        else:
            obj_cupones = []
            for cupon in empleado.codigos_descuento():
                obj_cupon = {}
                obj_cupon["id"] = cupon.id
                obj_cupon["codigo"] = empleado.nombre
                obj_cupon["canjeado"] = empleado.apellido
                obj_cupon["creado"] = empleado.direccion
                obj_cupon["actualizado"] = empleado.telefono
                obj_cupon["creado_por"] = serializers.serialize('json', cupon.creado_por)
                obj_cupon["actualizado_por"] = serializers.serialize('json', cupon.actualizado_por)
                obj_cupon["cliente"] = serializers.serialize('json', cupon.cliente)
                obj_cupon["descuento"] = serializers.serialize('json', cupon.descuento)
                obj_cupones.append(obj_cupon)

            obj_json['cupones'] = obj_cupones
            obj_json['code'] = 200
            obj_json['mensaje'] = "Empleado encontrado"

    data = json.dumps(obj_json)
    return HttpResponse(data, content_type='application/json')


# endregion

class dashboard_comercio(TemplateView):
    template_name = "arca/comercio/dashboard.html"

    def get(self, request, *args, **kwargs):
        context = super(dashboard_comercio, self).get_context_data(**kwargs)
        context = authorize(request, context)
        if not context.get('auth_comercio') and not context.get('auth_empleado'):
            return HttpResponseRedirect("/arca/login_comercio")
        else:
            return super(dashboard_comercio, self).render_to_response(context)


# region producto
def render__producto(request):
    context = Context()
    context = authorize(request, context)
    if context.get('auth_comercio'):
        id = request.GET.get('id')
        producto = None
        if id:
            producto = Producto.objects.filter(id=id).first()
        html = render_to_string('arca/comercio/_producto.html',
                                {'producto': producto})
        return HttpResponse(html)


@csrf_exempt
def save_producto(request):
    context = Context()
    context = authorize(request, context)
    if context.get('auth_comercio'):
        data = []
        obj_json = {'mensaje': 'ok', 'code': 200}
        codigo = request.POST.get('id')
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        descuento = request.POST.get('descuento')
        activo = request.POST.get('activo')

        if not nombre:
            obj_json['code'] = 400
            obj_json['mensaje'] = "Nombre invalido"
        elif not descripcion:
            obj_json['code'] = 400
            obj_json['mensaje'] = "Descripcion invalido"
        elif not precio:
            obj_json['code'] = 400
            obj_json['mensaje'] = "Precio invalido"
        elif not descuento:
            obj_json['code'] = 400
            obj_json['mensaje'] = "Descuento invalido"
        else:
            try:
                producto = Producto.objects.get(pk=int(codigo))
            except Exception, e:
                producto = Producto.objects.create(nombre=nombre, precio=precio)
            try:
                if producto:
                    comercio = context.get('auth_comercio')
                    producto.nombre = str(nombre)
                    producto.descripcion = str(descripcion)
                    producto.descuento = descuento
                    if len(request.FILES) > 0:
                        producto.imagen = request.FILES['imagen']
                    if not activo:
                        producto.activo = False
                    else:
                        producto.activo = True
                    producto.comercio = comercio
                    producto.save()
            except Exception, e:
                print e.message
                obj_json['code'] = 500
                obj_json['mensaje'] = "Ocurrio un error valido"
        data.append(obj_json)
        data = json.dumps(data)
        return HttpResponse(data, content_type='application/json')


@csrf_exempt
def render_producto(request):
    context = Context()
    context = authorize(request, context)
    if context.get('auth_comercio'):
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
        comercio = context.get('auth_comercio')

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


@csrf_exempt
def render_listado_productos(request):
    context = Context()
    context = authorize(request, context)
    if context.get('auth_comercio'):
        comercio = context.get('auth_comercio')
        productos = Producto.objects.filter(comercio=comercio).order_by('-activo')
        html = render_to_string('arca/comercio/_productos.html', {'productos': productos})
        return HttpResponse(html)


# endregion


class render_comercio_categoria(TemplateView):
    template_name = "arca/categoria_comercios.html"

    def get(self, request, *args, **kwargs):
        context = super(render_comercio_categoria, self).get_context_data(**kwargs)
        context = authorize(request, context)
        if not context.get('auth_comercio') and not context.get('auth_empleado'):
            return HttpResponseRedirect("/arca/login_comercio")
        else:
            categoria = request.GET.get('id')
            if categoria:
                c = Comercio_Categoria.objects.get(pk=int(categoria))
                context['comercios'] = Comercio.objects.filter(categoria=c)
            return super(render_comercio_categoria, self).render_to_response(context)
