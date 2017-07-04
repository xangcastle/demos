import json

from background_task import background
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

from inblensa.models import Import_Imventario, Import
from .models import *
import requests


class Index(TemplateView):
    template_name = "control/index.html"

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['apps'] = get_aplications(self.request.user)
        context['options'] = get_options(self.request.user)
        # actualizar_cliente()
        # actualizar_inventario()
        return context


class Calculator(TemplateView):
    template_name = "control/calculator.html"


def actualizar_inventario():
    url = 'http://inblensa.ddns.net:7779/Home/get_data_from_server'
    params = {'vista': 'view_info_migration'}
    response = requests.post(url, params=params)
    assert response.status_code == 200
    json_data = response.json()
    i = 321

    for d in json_data:
        i += 1

        if not d["producto_existencia"]:
            existencia = 0
        else:
            existencia = d["producto_existencia"]

        if not d["producto_costo"]:
            costo = 0
        else:
            costo = d["producto_costo"]

        if not d["producto_precio"]:
            precio = 0
        else:
            precio = d["producto_precio"]
        Import_Imventario.objects.get_or_create(id=i,
                                                razon_social=d["razon_social"],
                                                producto_codigo=d["producto_codigo"],
                                                producto_serie=d["producto_serie"],
                                                producto_nombre=d["producto_nombre"],
                                                producto_existencia=existencia,
                                                producto_costo=costo,
                                                producto_precio=precio,
                                                producto_marca=d["producto_marca"],
                                                producto_categoria=d["producto_categoria"],
                                                producto_medida=d["producto_medida"],
                                                bodega=d["bodega"])


def actualizar_cliente():
    url = 'http://inblensa.ddns.net:7779/Home/get_data_from_server'
    params = {'vista': 'view_info_migration_cliente'}
    response = requests.post(url, params=params)
    assert response.status_code == 200
    json_data = response.json()
    i = 321
    for d in json_data:
        i += 1
        print d["CLAVE"]
        if d['CLAVE'] == '96':
            print 'encontrado!'
        Import.objects.get_or_create(id=i,
                                     razon_social=d["razon_social"],
                                     numero_ruc=d["numero_ruc"],
                                     nombre=d["nombre"],
                                     identificacion=d["identificacion"],
                                     telefono=d["telefono"],
                                     direccion=d["direccion"],
                                     contacto=d["contacto"])


@csrf_exempt
def agregar_registro(request):
    obj_json = {}
    tag = request.POST.get("tag", None)
    mensaje = request.POST.get("mensaje", None)
    fecha = request.POST.get("fecha", None)
    usuario = request.POST.get("usuario", None)

    if not tag:
        obj_json['code'] = 400
        obj_json['mensaje'] = "TAG no encontrada"
    elif not mensaje:
        obj_json['code'] = 400
        obj_json['mensaje'] = "Mensaje no encontrado"
    elif not fecha:
        obj_json['code'] = 400
        obj_json['mensaje'] = "Fecha no encontrado"
    elif not usuario:
        obj_json['code'] = 400
        obj_json['mensaje'] = "Fecha no encontrado"
    else:
        registro, c = Registro.objects.get_or_create(
            tag=tag,
            mensaje=mensaje,
            fecha=fecha,
            usuario=usuario
        )
        if not registro:
            obj_json['code'] = 500
            obj_json['mensaje'] = "No fue posible crear el registro"
        else:
            obj_json['code'] = 200
            obj_json['mensaje'] = "Registro creado exitosamente"
    data = json.dumps(obj_json)
    return HttpResponse(data, content_type='application/json')
