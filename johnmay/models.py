from __future__ import unicode_literals

from django.db import models
from base.models import Entidad
from django.contrib.auth.models import User


class Perfil(models.Model):
    user = models.OneToOneField(User)
    sucursales = models.ManyToManyField('Sucursal')
    bodegas = models.ManyToManyField('Bodega')


class Sucursal(Entidad):
    pass


class Bodega(Entidad):
    sucursal = models.ForeignKey(Sucursal)


class Producto(Entidad):
    descripcion = models.CharField(max_length=400)
    costo = models.FloatField(default=0.0)
    precio = models.FloatField(default=0.0)
    marca = models.ForeignKey('Marca')
    categoria = models.ForeignKey('Categoria')


class Marca(Entidad):
    pass


class Categoria(Entidad):
    pass


class Existencia(models.Model):
    producto = models.ForeignKey(Producto)
    bodega = models.ForeignKey(Bodega)
    cantidad = models.FloatField(default=0.0)
    precio_pactado = models.FloatField(default=0.0)


TIPO_DOC = (
    ('101', 'OTRAS ENTRADAS AL INVENTARIO'),
    ('102', 'OTRAS SALIDAS AL INVENTARIO'),

    ('201', 'REQUIZA DE ENTRADA'),
    ('202', 'REQUIZA DE SALIDA'),
)


class Documento(models.Model):
    fecha = models.DateField()
    numero = models.CharField(max_length=6, default='')
    user = models.ForeignKey(User)
    sucursal = models.ForeignKey(Sucursal, null=True)
    tipo_doc = models.CharField(max_length=3, null=True, choices=TIPO_DOC)
    comentario = models.CharField(max_length=400)

    def __unicode__(self):
        return "%s - %s" % (self.tipo_doc, self.numero)

    def detalles(self):
        return Detalle.objects.filter(cabecera=self)


class Detalle(models.Model):
    cabecera = models.ForeignKey(Documento)
    producto = models.ForeignKey(Producto)
    bodega = models.ForeignKey(Bodega)
    cantidad = models.FloatField(default=0.0)


