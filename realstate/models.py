from __future__ import unicode_literals

import datetime
from string import upper

import realstate
from django.db import models
from django.db.models import Sum, Max
from django.contrib.auth.models import User
from django.http import HttpResponse
from fontawesome.fields import IconField
from geoposition.fields import GeopositionField
import json
from django.core import serializers



def format_fecha(fecha):
    return "%s-%s-%s" % (fecha.year, fecha.month, fecha.day)


def get_media_url(self, filename):
    clase = self.__class__.__name__
    code = str(self.id)
    return '%s/%s/%s' % (clase, code, filename)


class Departamento(models.Model):
    nombre = models.CharField(max_length=50, null=True, blank=True)

    def __unicode__(self):
        return "%s" % self.nombre

class Municipio(models.Model):
    nombre = models.CharField(max_length=50, null=True, blank=True)
    departamento = models.ForeignKey(Departamento)

    def __unicode__(self):
        return "%s - %s" % (self.departamento, self.nombre)

class Localidad(models.Model):
    nombre = models.CharField(max_length=50, null=True, blank=True)
    municipio = models.ForeignKey(Municipio)

    def __unicode__(self):
        return "%s - %s" % (self.municipio, self.nombre)

    class Meta:
        verbose_name_plural = "localidades"



# region PROPIETARIO
class Propietario(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=True)
    apellido = models.CharField(max_length=100, null=True, blank=True)
    razon_social = models.CharField(max_length=100, null=True, blank=True)
    is_corporative = models.BooleanField()

    def __unicode__(self):
        if self.is_corporative:
            return self.razon_social
        else:
            return "%s %s" % (self.nombre, self.apellido)

    def propiedades(self):
        return Propiedad.objects.filter(propietario=self)

    def datos_contacto(self):
        return Propietario_Contacto.objects.filter(propietario=self)

    def save(self, *args, **kwargs):
        if self.razon_social:
            self.is_corporative = True
        else:
            self.is_corporative = False
        super(Propietario, self).save()

    class Meta:
        verbose_name = "opcion"
        verbose_name_plural = "Propietarios"


class Tipo_Contacto(models.Model):
    tipo = models.CharField(max_length=100)
    icono = IconField()

    class Meta:
        verbose_name = "opcion"
        verbose_name_plural = "Tipos de Contacto"

    def __unicode__(self):
        return "%s" % (self.tipo)


class Propietario_Contacto(models.Model):
    propietario = models.ForeignKey(Propietario, null=False, blank=False)
    tipo_contacto = models.ForeignKey(Tipo_Contacto, null=False, blank=False)
    valor = models.CharField(max_length=100)


# endregion


class Propiedad(models.Model):
    localidad = models.ForeignKey(Localidad, null=True, blank=True)
    direccion = models.TextField(max_length=500)
    position = GeopositionField(null=True, blank=True)
    nombre = models.CharField(max_length=100, null=False, blank=False)
    area = models.FloatField(null=True, blank=True)
    habitaciones = models.IntegerField(null=True, blank=True)
    pisina = models.NullBooleanField(null=True, blank=True)
    cochera = models.IntegerField(default=0, null=True, blank=True)
    banios = models.FloatField(default=0, null=True, blank=True)
    plantas = models.IntegerField(default=1, null=True, blank=True)
    propietario = models.ForeignKey(Propietario, null=True, blank=True)
    #galerias = models.ManyToManyField(Galeria, null=True, blank=True)
    ESTADOS_NEGOCIO = (('PARA RENTA', 'PARA RENTA'),
                       ('PARA VENTA', 'PARA VENTA'),
                       )
    estado_negocio = models.CharField(max_length=65, null=True, blank=True,
                                      choices=ESTADOS_NEGOCIO)
    valor = models.FloatField(null=True, blank=True)
    portada = models.ImageField(upload_to=get_media_url, null=True, blank=True)
    descripcion = models.TextField(max_length=800, null=True, blank=True)

    def portada_url(self):
        if self.portada:
            return self.portada.url
        else:
            return "/static/wp-content/uploads/2015/07/property-12-660x600.jpg"

    def fotos(self):
        return Foto.objects.filter(propiedad=self)

    def extras(self):
        return Propiedad_Extra.objects.filter(propiedad=self)

    class Meta:
        verbose_name_plural = "propiedades"

# region GALERIA
class Galeria(models.Model):
    nombre = models.CharField(max_length=50, null=False, blank=False)
    fecha = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    usuario = models.ForeignKey(User, null=False, blank=False)

    def fotos(self):
        return Foto.objects.filter(propietario=self)


class Foto(models.Model):
    #galeria = models.ForeignKey(Galeria, null=True, blank=True)
    propiedad = models.ForeignKey(Propiedad, null=True, blank=True)
    foto = models.ImageField(upload_to=get_media_url, null=True, blank=True)

class Propiedad_Extra(models.Model):
    propiedad = models.ForeignKey(Propiedad, null=True, blank=True)
    nombre =  models.CharField(max_length=100, null=False, blank=False)
    valor =  models.CharField(max_length=300, null=False, blank=False)
# endregion
