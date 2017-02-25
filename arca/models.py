from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.

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
    telefono = models.CharField(max_length=10)
    categoria = models.ForeignKey(Comercio_Categoria)
    propietario = models.ForeignKey(User)

class Promocion(models.Model):
    nombre = models.CharField(max_length=100)
    banner = models.ImageField(upload_to=get_media_url, null=True, blank=True)
    commercio = models.ForeignKey(Commercio)

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
    precio =  models.FloatField()
    descuento = models.FloatField(null=True, blank=True)
    imagen = models.ImageField(upload_to=get_media_url, null=True, blank=True)

