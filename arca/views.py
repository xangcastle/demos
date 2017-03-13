# coding=utf-8
from django.template import Context
import json

from django import forms

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
                response.set_cookie('auth_comercio', comercio.id)
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
                response.set_cookie('auth_empleado', empleado.id)
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


# region COMERCIO ADMIN
class negocio_form(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    password_new = forms.CharField(label='Nueva Contraseña', max_length=100, required=False,
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password_conf = forms.CharField(label='Confirmar Contraseña', max_length=100, required=False,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Comercio
        fields = ['nombre', 'direccion', 'telefono', 'identificacion', 'categoria', 'logo', 'username', 'password']

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
        if self.cleaned_data['password'] == comercio.password:
            if len(self.cleaned_data['password_new']) > 0:
                comercio.password = self.cleaned_data['password_new']
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


class edit_comercio(TemplateView):
    template_name = "arca/comercio/registrar_negocio.html"

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
            comercio = form.save(commit=False)
            comercio.save()
            context["form"] = form
            context["success_message"] = "Datos actualizados exitosamente!"
            return redirect("mi_comercio")
        else:
            context["form"] = form

        return super(edit_comercio, self).render_to_response(context)

#region REGISTRO DEL COMERCIO
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
        comercio.nombre = nombre_empresa
        comercio.direccion = direccion_empresa
        comercio.telefono = telefono_empresa
        comercio.username = usuario_email
        comercio.password = usuario_password
        comercio.nombre = usuario_nombre + " " + usuario_apellido
        comercio.save()

        comercio = autenticate(Comercio(), usuario_email, usuario_password)

        response = render(request, 'arca/comercio/mi_comercio.html', {"comercio": comercio})
        if comercio:
            response.set_cookie('auth_comercio', comercio.id)

        return response
#endregion

# endregion
# region DESCUENTOS
def render_descuento(request):
    id = request.GET.get('id')
    if id:
        descuento = Descuento.objects.filter(id=id).first()
    else:
        descuento = Descuento()

    descuento.comercio = request.user.perfil.comercio()
    html = render_to_string('arca/comercio/_descuento.html',
                            {'descuento': descuento})
    return HttpResponse(html)


def render_listado_descuento(request):
    context = Context()
    context = authorize(request, context)
    if context.get('auth_comercio'):
        comercio = context.get('auth_comercio')
        descuentos = Descuento.objects.filter(comercio=comercio).order_by('-activo')
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


# endregion
# region CUPONES
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
    descuentos = Descuento.objects.filter(comercio=request.user.perfil.comercio(), activo=True)
    html = render_to_string('arca/comercio/_cupon.html',
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
                    empleado.password = password
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
                                                                          password=password)

                        obj_json['code'] = 200
                        obj_json['mensaje'] = "Empleado registrado exitosamente!"

    data.append(obj_json)
    data = json.dumps(data)
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