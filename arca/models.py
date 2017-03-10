from __future__ import unicode_literals

import datetime
import uuid

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils.timezone import utc
from geoposition.fields import GeopositionField
from social_django.models import UserSocialAuth

def get_media_url(self, filename):
    clase = self.__class__.__name__
    code = str(self.id)
    return '%s/%s/%s' % (clase, code, filename)

class CustomUserSocialAuth(UserSocialAuth):
    image = models.CharField(max_length=500, null=True,blank=True)

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to=get_media_url, null=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    direccion = models.CharField(max_length=500, null=True, blank=True)

    def imagen_url(self):
        if self.foto:
            if "http" in self.foto.url:
                return str(self.foto)
            else:
                return self.foto.url
        else:
            return "/media/foto-no-disponible.jpg"

    def comercio(self):
        co = Comercio.objects.filter(propietario=self.user).first()
        if not co:
            empleado = Empleado.objects.filter(usuario=self.user, fecha_baja=None).first()
            if empleado:
                co=empleado.comercio
        return co




# Create your models here.
class Comercio_Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categorias de comercio"
        verbose_name="Categoria"

    def __unicode__(self):
        return self.nombre


class Comercio(models.Model):
    nombre = models.CharField(max_length=100,null=True, blank=True)
    direccion = models.CharField(max_length=500,null=True, blank=True)
    position = GeopositionField(null=True, blank=True)
    telefono = models.CharField(max_length=10, null=True, blank=True)
    categoria = models.ForeignKey(Comercio_Categoria,null=True, blank=True, related_name="rel_comercio_categoria")
    identificacion = models.CharField(max_length=50, null=True, blank=True)
    propietario = models.ForeignKey(User, related_name="rel_comercio_usuario")
    logo = models.ImageField(upload_to=get_media_url, null=True, blank=True)
    tiene_descuento_vigencia = models.BooleanField(default=False)
    tiene_descuento_compra_minima = models.BooleanField(default=False)
    tiene_servicio_afiliacion = models.BooleanField(default=False)
    tiene_servicio_crm = models.BooleanField(default=False)

    def __unicode__(self):
        return self.nombre

    def usuarios_empleados(self):
        usuarios=[]
        empleados = Empleado.objects.filter(comercio=self)
        for empleado in empleados:
            usuarios.append(empleado.usuario)
        usuarios.append(self.propietario)
        return  usuarios

class Empleado(models.Model):
    usuario = models.ForeignKey(User)
    comercio = models.ForeignKey(Comercio)
    fecha_alta = models.DateTimeField(auto_now_add=True)
    fecha_baja = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.usuario.username




# DEFINICION GENERAL DE UN DESCUENTO
class Descuento(models.Model):
    comercio = models.ForeignKey(Comercio)
    nombre = models.CharField(max_length=100,null=True, blank=True)
    porcentaje_descuento = models.FloatField()
    vigencia = models.IntegerField()  # VIGENIA DEL DESCUENTO EN DIAS ANTES DE VENCIMIENTO

    desc_dia_vigencia = models.IntegerField(null=True, blank=True)  # (PRO) ii.	Descuentos Segun Dias de Vigencia:
    desc_dia_vigencia_porc_inf = models.FloatField(null=True, blank=True)  # (PRO) porcentaje descuento si compra antes de este dia
    desc_dia_vigencia_porc_sup = models.FloatField(null=True, blank=True)  # (PRO) porcentaje descuento si compra despues de este dia
    desc_compra_minima = models.FloatField(null=True, blank=True)  # (PRO) iii.	Descuentos Segun Monto de Compra

    desc_compra_minima_porc_inf = models.FloatField(null=True, blank=True)  # (PRO) porcentaje descuento si monto compra < compra_minima
    desc_compra_minima_porc_sup = models.FloatField(null=True, blank=True)  # (PRO) porcentaje descuento si monto compra > compra_minima

    tipo_cambio = models.FloatField(default=1)  # Campo para soportar multimoneda DOLAR/CORDOBA
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
        super(Descuento, self).save(*args, **kwargs)


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
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        dias_transcurridos = (self.creado - now).days
        dias_vence = self.descuento.vigencia - dias_transcurridos
        if dias_vence == 0:
            return "vence Hoy"
        elif dias_vence > 0:
            return "vence en %s dias" % dias_vence
        else:
            return "vencido hace %s dias" % dias_vence

    def save(self, *args, **kwargs):
        li = []
        li.append(kwargs.pop('user', 1))
        usuario = User.objects.get(id=li[0])
        if not self.creado_por:
            self.creado_por = usuario
        self.actualizado_por = usuario
        super(Codigo_Descuento, self).save(*args, **kwargs)

class Publicidad(models.Model):
    nombre = models.CharField(max_length=100)
    banner = models.ImageField(upload_to=get_media_url, null=True, blank=True)
    commercio = models.ForeignKey(Comercio)
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
