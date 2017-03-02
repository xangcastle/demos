from __future__ import unicode_literals

import datetime
import uuid

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from geoposition.fields import GeopositionField


def get_media_url(self, filename):
    clase = self.__class__.__name__
    code = str(self.id)
    return '%s/%s/%s' % (clase, code, filename)


# Create your models here.
class Comercio_Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)


class Commercio(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=500)
    position = GeopositionField(null=True, blank=True)
    telefono = models.CharField(max_length=10)
    categoria = models.ForeignKey(Comercio_Categoria)
    propietario = models.ForeignKey(User)
    tiene_descuento_vigencia = models.BooleanField(default=False)
    tiene_descuento_compra_minima = models.BooleanField(default=False)
    tiene_servicio_afiliacion = models.BooleanField(default=False)
    tiene_servicio_crm = models.BooleanField(default=False)


class Empleado(models.Model):
    usuario = models.ForeignKey(User)
    comercio = models.ForeignKey(Commercio)
    fecha_alta = models.DateTimeField(auto_now_add=True)
    fecha_baja = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        li = []
        li.append(kwargs.pop('user', 1))
        usuario = User.objects.get(id=li[0])
        # SE DA DE BAJA AL EMPLEADO SI ESTA EN OTRO COMERCIO
        ck_empleado = Empleado.objects.filter(usuario=self.usuario)
        if ck_empleado:
            for empleado in ck_empleado:
                if empleado.comercio != self.comercio:
                    empleado.fecha_baja = datetime.date.now()

        Empleado.objects.get_or_create(usuario=self.usuario, comercio=self.comercio)


# DEFINICION GENERAL DE UN DESCUENTO
class Descuento(models.Model):
    commercio = models.ForeignKey(Commercio)
    porcentaje_descuento = models.FloatField()
    vigencia = models.IntegerField()  # VIGENIA DEL DESCUENTO EN DIAS ANTES DE VENCIMIENTO
    desc_dia_vigencia = models.IntegerField()  # (PRO) ii.	Descuentos Segun Dias de Vigencia:
    desc_dia_vigencia_porc_inf = models.FloatField()  # (PRO) porcentaje descuento si compra antes de este dia
    desc_dia_vigencia_porc_sup = models.FloatField()  # (PRO) porcentaje descuento si compra despues de este dia
    desc_compra_minima = models.FloatField()  # (PRO) iii.	Descuentos Segun Monto de Compra
    desc_compra_minima_porc_inf = models.FloatField()  # (PRO) porcentaje descuento si monto compra < compra_minima
    desc_compra_minima_porc_sup = models.FloatField()  # (PRO) porcentaje descuento si monto compra > compra_minima
    tipo_cambio = models.FloatField()  # Campo para soportar multimoneda DOLAR/CORDOBA
    activo = models.BooleanField(default=True)
    creado_por = models.ForeignKey(User, related_name="Descuento_Usuario_Creacion")
    actualizado_por = models.ForeignKey(User, related_name="Descuento_Usuario_Actualizacion")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        li = []
        li.append(kwargs.pop('user', 1))
        usuario = User.objects.get(id=li[0])
        if not self.creado_por:
            self.creado_por = usuario
        self.actualizado_por = usuario
        self.save()


# CODIGO DE DESCUENTO QUE SE GENERA PARA UN CLIENTE
class Codigo_Descuento(models.Model):
    codigo = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    descuento = models.ForeignKey(Descuento)
    cliente = models.ForeignKey(User, related_name="Codigo_Descuento_Usuario_Cliente", null=True, blank=True)
    canjeado = models.BooleanField(default=False)  # indica si este codigo ya fue canjeado por el cliente
    creado_por = models.ForeignKey(User, related_name="Codigo_Descuento_Usuario_Creacion")
    actualizado_por = models.ForeignKey(User, related_name="Codigo_Descuento_Usuario_Actualizacion")
    creado = models.DateTimeField(
        auto_now_add=True)  # tomando en cuenta la creacion se determina segun vigencia su validez
    actualizado = models.DateTimeField(auto_now=True)

    def valido(self):
        dias_transcurridos = (self.creado - datetime.date.now()).days
        return self.descuento.vigencia <= dias_transcurridos

    def vence_en(self):
        dias_transcurridos = (self.creado - datetime.date.now()).days
        dias_vence = self.descuento.vigencia - dias_transcurridos
        if dias_vence == 0:
            return "Hoy"
        elif dias_vence > 0:
            return "%s dias" % dias_vence
        else:
            return "hace %s dias" % dias_vence


class Publicidad(models.Model):
    nombre = models.CharField(max_length=100)
    banner = models.ImageField(upload_to=get_media_url, null=True, blank=True)
    commercio = models.ForeignKey(Commercio)
    activo = models.BooleanField(default=True)
    creado_por = models.ForeignKey(User, related_name="Publicidad_Usuario_Creacion")
    actualizado_por = models.ForeignKey(User, related_name="Publicidad_Usuario_Actualizacion")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    # fecha en que se da baja definitiva a la publicidad puede
    # servir para cobrar el servicio (PRO) v.	Publicidad
    baja = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        li = []
        li.append(kwargs.pop('user', 1))
        usuario = User.objects.get(id=li[0])
        if not self.creado_por:
            self.creado_por = usuario
        self.actualizado_por = usuario
        self.save()


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
    precio = models.FloatField()
    descuento = models.FloatField(null=True, blank=True)  # precio promocional
    imagen = models.ImageField(upload_to=get_media_url, null=True, blank=True)
