from django.contrib.auth import authenticate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.serializers.json import DjangoJSONEncoder
from django.forms import model_to_dict
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from geoposition import Geoposition
from realstate.models import *
from django.core.mail import EmailMessage


def inicio(request):
    return HttpResponseRedirect("/app")


class index(TemplateView):
    template_name = "propiedades.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        page = request.GET.get('page', 1)

        propiedades_list = Propiedad.objects.all()

        for k, vals in request.GET.lists():
            for v in vals:
                if not k == 'page':
                    propiedades_list = propiedades_list.filter(**{k: v})

        paginator = Paginator(propiedades_list, 3)
        try:
            propiedades = paginator.page(page)
        except PageNotAnInteger:
            propiedades = paginator.page(1)
        except EmptyPage:
            propiedades = paginator.page(paginator.num_pages)

        context['propiedades'] = propiedades
        return super(index, self).render_to_response(context)


def get_usuario(request):
    obj_json = {}

    username = request.GET.get('username', '')
    password = request.GET.get('password', '')
    user = authenticate(username=username, password=password)
    if user:
        obj_json['code'] = "200"
        obj_json['usuario'] = json.loads(serializers.serialize('json', [user, ]))
    else:
        obj_json['code'] = "500"
        obj_json['mensaje'] = "Usuario no encontrado"
    return HttpResponse(json.dumps(obj_json), content_type='application/json')


class get_propiedades(TemplateView):
    def get(self, request, *args, **kwargs):
        propiedades = Propiedad.objects.all()
        data = []
        for propiedad in propiedades:
            obj_json = {}
            obj_json['id_propiedad'] = propiedad.id
            obj_json['nombre'] = propiedad.nombre
            obj_json['direccion'] = propiedad.direccion
            obj_json['area'] = propiedad.area
            obj_json['habitaciones'] = propiedad.habitaciones
            obj_json['pisina'] = propiedad.pisina
            obj_json['cochera'] = propiedad.cochera
            obj_json['banios'] = propiedad.banios
            obj_json['plantas'] = propiedad.plantas
            obj_json['estado_negocio'] = propiedad.estado_negocio
            obj_json['valor'] = propiedad.valor
            obj_json['portada'] = propiedad.portada_url()
            obj_json['descripcion'] = propiedad.descripcion

            if propiedad.propietario:
                propietario_json = {}
                propietario_json['id_propietario'] = propiedad.propietario.id
                propietario_json['nombre'] = propiedad.propietario.nombre
                propietario_json['apellido'] = propiedad.propietario.apellido
                propietario_json['razon_social'] = propiedad.propietario.razon_social
                obj_json['propietario'] = propietario_json

            fotos = []
            for foto in propiedad.fotos():
                foto_json = {}
                foto_json['id_foto'] = foto.id
                foto_json['url'] = foto.foto.url
                fotos.append(foto_json)
            obj_json['fotos'] = fotos

            data.append(obj_json)

        data = json.dumps(data)
        response = HttpResponse(data, content_type='application/json')
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response

@csrf_exempt
def get_propiedad(request):
    obj_json = {}
    obj_json['id_propiedad'] = request.POST.get('id_propiedad', 0)
    obj_json['nombre'] = request.POST.get('nombre', '')
    obj_json['direccion'] = request.POST.get('direccion', '')
    obj_json['area'] = request.POST.get('area', 0)
    obj_json['habitaciones'] = request.POST.get('habitaciones', 0)
    obj_json['banios'] = request.POST.get('banios', 0)
    obj_json['cocheras'] = request.POST.get('cocheras', 0)
    obj_json['plantas'] = request.POST.get('plantas', 0)
    obj_json['valor'] = request.POST.get('valor', 0)
    obj_json['estado_negocio'] = request.POST.get('estado_negocio', '')
    obj_json['id_propietario'] = request.POST.get('id_propietario', 0)
    obj_json['descripcion'] = request.POST.get('descripcion', '')
    obj_json['Latitude'] = request.POST.get('Latitude', 0)
    obj_json['Longitude'] = request.POST.get('Longitude', 0)
    obj_json['Mensaje'] = ''
    propietario=Propietario.objects.filter(id=int(obj_json['id_propietario'])).first()
    if not propietario:
        obj_json['code'] = 400
        obj_json['Mensaje'] = "Propietario no encontrado"
    else:
        propiedad = Propiedad.objects.filter(id=int(obj_json['id_propiedad'])).first()
        if not propiedad:
            propiedad, create = Propiedad.objects.get_or_create(direccion=smart_str(obj_json['direccion']))


        propiedad.nombre = smart_str(obj_json['nombre'])
        propiedad.direccion = smart_str(obj_json['direccion'])
        propiedad.area = float(obj_json['area'])
        propiedad.habitaciones = int(obj_json['habitaciones'])
        propiedad.banios = float(obj_json['banios'])
        propiedad.cochera = int(obj_json['cocheras'])
        propiedad.plantas = int(obj_json['plantas'])
        propiedad.valor = float(obj_json['valor'])
        propiedad.estado_negocio = smart_str(obj_json['estado_negocio'])
        propiedad.descripcion = smart_str(obj_json['descripcion'])
        propiedad.position = Geoposition(obj_json['Latitude'],
                                         obj_json['Longitude'])
        propiedad.propietario=propietario

        try:
            propiedad.portada = request.FILES['portada']
        except:
            pass

        propiedad.save()
        obj_json['code'] = 200
        obj_json['id_propiedad'] = propiedad.id
        obj_json['Mensaje'] = "Propiedad registrada"
    data = json.dumps(obj_json)
    return HttpResponse(data, content_type='application/json')

@csrf_exempt
def get_foto_propiedad(request):
    obj_json = {}
    obj_json['id_propiedad'] = request.POST.get('id_propiedad', 0)
    propiedad = Propiedad.objects.get(id=int(obj_json['id_propiedad']))
    if not propiedad:
        obj_json['Mensaje'] = "Propiedad no encontrada"
        obj_json['code'] = 400
    else:
        try:
            img = Foto.objects.get_or_create(foto=request.FILES['foto'])
            img.propiedad = propiedad
            img.save()
            obj_json['Mensaje'] = "Foto registrada"
            obj_json['code'] = 200
        except:
            obj_json['Mensaje'] = "Foto es requerida"
            obj_json['code'] = 400

    data = json.dumps(obj_json)
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def get_propietario(request):
    obj_json = {}
    obj_json['nombre'] = request.POST.get('nombre', '')
    obj_json['apellido'] = request.POST.get('apellido', '')
    obj_json['razon_social'] = request.POST.get('razon_social', '')
    if obj_json['nombre'] == '' and obj_json['razon_social'] == '':
        obj_json['Mensaje'] = "Nombre o Razon social requerida"
        obj_json['code'] = 400
    else:
        propietario = Propietario.objects.get_or_create(nombre=str(obj_json['nombre']),
                                                        apellido=str(obj_json['apellido']),
                                                        razon_social=str(obj_json['razon_social']))
        obj_json['id_propietario'] = propietario.id
        obj_json['Mensaje'] = "Propietario registrado"
        obj_json['code'] = 200

    data = json.dumps(obj_json)
    return HttpResponse(data, content_type='application/json')


class show_propiedad(TemplateView):
    template_name = "propiedad.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        propiedad = Propiedad.objects.get(id=request.GET.get('id'))
        context['propiedad'] = propiedad
        return super(show_propiedad, self).render_to_response(context)


class enviar_mail(TemplateView):
    def post(self, request, *args, **kwargs):
        subject = '%s Informacion de casa %s' % (request.POST.get('name', ''), request.POST.get('property_title', ''))

        message = '%s Nombre: %s Telefono Contacto: %s Email: %s' % (request.POST.get('message', ''),
                                                                     request.POST.get('name', ''),
                                                                     request.POST.get('from_email', ''),
                                                                     request.POST.get('contact-number', ''))
        email = EmailMessage(subject, message, to = ['cesarabel@deltacopiers.com', 'jwgarcia003@gmail.com'])
        email.send()




