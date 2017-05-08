
from __future__ import unicode_literals
import datetime
import uuid
from django.utils.html import mark_safe
from django.db.models import Avg

from arca.crypter import *
from django.db import models
from django.utils.timezone import utc
from geoposition.fields import GeopositionField


def ifnull(var, opt, oth=None):
    if not var:
        return opt
    else:
        if oth:
            return oth
        else:
            return var

def get_media_url(self, filename):
    clase = self.__class__.__name__
    code = str(self.id)
    return '%s/%s/%s' % (clase, code, filename)


class Login(models.Model):
    username = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.username


def autenticate(login, username, password):
    '''
    login is a Login instance...
    '''
    try:
        return type(login).objects.get(username=username, password=encrypt_val(password))
    except:
        return None


class Usuario(Login):
    '''
    Este es el usuario de la app de descuentos
    '''
    nombre = models.CharField(max_length=100, null=True, blank=True)
    apellido = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    age = models.PositiveIntegerField(null=True)
    gender = models.CharField(max_length=15, null=True)
    foto = models.ImageField(upload_to=get_media_url, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    direccion = models.CharField(max_length=500, null=True, blank=True)
    codigo = models.CharField(max_length=100, blank=True, default=uuid.uuid4)

    def imagen_url(self):
        if self.foto:
            if "http" in self.foto.url:
                return str(self.foto)
            else:
                return self.foto.url
        else:
            return "/media/foto-no-disponible.jpg"

    def cupones(self):
        return Codigo_Descuento.objects.filter(cliente=self)


class Comercio_Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categorias de comercio"
        verbose_name = "Categoria"

    def __unicode__(self):
        return self.nombre


class Comercio(Login):
    '''
    Este es el usuario dueno de negocio
    '''
    nombre = models.CharField(max_length=100, null=True, blank=True)
    nombre_propietario = models.CharField(max_length=100, null=True, blank=True)
    direccion = models.TextField(max_length=500, null=True, blank=True)
    position = GeopositionField(null=True, blank=True)
    telefono = models.CharField(max_length=10, null=True, blank=True)
    categoria = models.ForeignKey(Comercio_Categoria, null=True, blank=True, related_name="rel_comercio_categoria")
    identificacion = models.CharField(max_length=50, null=True, blank=True)
    logo = models.ImageField(upload_to=get_media_url, null=True, blank=True)
    baner = models.ImageField(upload_to=get_media_url, null=True, blank=True)
    tiene_descuento_vigencia = models.BooleanField(default=False)
    tiene_descuento_compra_minima = models.BooleanField(default=False)
    tiene_servicio_afiliacion = models.BooleanField(default=False)
    tiene_servicio_crm = models.BooleanField(default=False)

    def __unicode__(self):
        return self.nombre

    def empleados(self):
        empleados = Empleado.objects.filter(comercio=self)
        return empleados

    def descuentos(self):
        return Descuento.objects.filter(comercio=self)

    def productos(self):
        return Producto.objects.filter(comercio=self)

    def rating(self):
        valoracion = Comercio_Rating.objects.filter(comercio=self).aggregate(Avg('rating'))
        if not valoracion or  valoracion['rating__avg'] is None or valoracion<1:
            return 1
        else:
            return int(valoracion['rating__avg'])

    def thumbnai(self):
        if self.logo:
            return mark_safe('<img src="%s"></img>' % self.logo.url)
        else:
            return mark_safe('<img src="%s"></img>' % '/media/no_image.jpg')

class Comercio_Rating(models.Model):
    comercio=models.ForeignKey(Comercio)
    usuario=models.ForeignKey(Usuario)
    rating=models.IntegerField(default=1)



class Empleado(Login):
    '''
    Este es el usuario que trabaja en un negocio
    '''
    comercio = models.ForeignKey(Comercio)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    apellido = models.CharField(max_length=100, null=True, blank=True)
    direccion = models.CharField(max_length=500, null=True, blank=True)
    telefono = models.CharField(max_length=10, null=True, blank=True)
    fecha_alta = models.DateTimeField(auto_now_add=True)
    fecha_baja = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return "%s %s" % (self.nombre, self.apellido)

    def codigos_descuento(self):
        return Codigo_Descuento.objects.filter(descuento__in=self.comercio.descuentos())

    def cupones(self):
        return Codigo_Descuento.objects.filter(descuento__in=self.comercio.descuentos(),
                                                creado_por=self)


class Descuento(models.Model):
    '''
    Es el tipo de descuento que oferta el comercio
    '''
    comercio = models.ForeignKey(Comercio)
    es_gratuito = models.BooleanField(default=False)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    porcentaje_descuento = models.FloatField()
    vigencia = models.IntegerField()  # VIGENIA DEL DESCUENTO EN DIAS ANTES DE VENCIMIENTO

    desc_dia_vigencia = models.IntegerField(null=True, blank=True)  # (PRO) ii.	Descuentos Segun Dias de Vigencia:
    desc_dia_vigencia_porc_inf = models.FloatField(null=True,
                                                   blank=True)  # (PRO) porcentaje descuento si compra antes de este dia
    desc_dia_vigencia_porc_sup = models.FloatField(null=True,
                                                   blank=True)  # (PRO) porcentaje descuento si compra despues de este dia

    desc_compra_minima = models.FloatField(null=True, blank=True)  # (PRO) iii.	Descuentos Segun Monto de Compra
    desc_compra_minima_porc_inf = models.FloatField(null=True,
                                                    blank=True)  # (PRO) porcentaje descuento si monto compra < compra_minima
    desc_compra_minima_porc_sup = models.FloatField(null=True,
                                                    blank=True)  # (PRO) porcentaje descuento si monto compra > compra_minima

    tipo_cambio = models.FloatField(default=1)  # Campo para soportar multimoneda DOLAR/CORDOBA
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)


class Codigo_Descuento(models.Model):
    '''
    Cada cupon que se ha generado para los usuarios de la app
    si importar de que tipo sean
    '''
    codigo = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    descuento = models.ForeignKey(Descuento)
    canjeado = models.BooleanField(default=False)  # indica si este codigo ya fue canjeado por el cliente
    cliente = models.ForeignKey(Usuario, null=True, blank=True)  # indica el cliente al que se dio este codigo
    creado = models.DateTimeField(
        auto_now_add=True)  # tomando en cuenta la creacion se determina segun vigencia su validez
    actualizado = models.DateTimeField(auto_now=True)
    creado_por = models.ForeignKey(Empleado, null=True, blank=True, related_name="Descuento_Empleado_Create")
    actualizado_por = models.ForeignKey(Empleado, null=True, blank=True, related_name="Descuento_Empleado_Update")

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


class Publicidad(models.Model):
    nombre = models.CharField(max_length=100)
    banner = models.ImageField(upload_to=get_media_url, null=True, blank=True)
    commercio = models.ForeignKey(Comercio)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    # fecha en que se da baja definitiva a la publicidad puede
    # servir para cobrar el servicio (PRO) v.	Publicidad
    baja = models.DateTimeField(null=True, blank=True)


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
    precio = models.FloatField()
    descuento = models.FloatField(null=True, blank=True)  # precio promocional
    imagen = models.ImageField(upload_to=get_media_url, null=True, blank=True)
    comercio = models.ForeignKey(Comercio, null=True, blank=True)
    activo = models.BooleanField(default=True)


class Factura(models.Model):
    documento = models.TextField(null=True, blank=True)
    comercio = models.ForeignKey(Comercio, null=True, blank=True)
    monto = models.FloatField(null=True, blank=True)
    descuento = models.FloatField(null=True, blank=True)
    cupon = models.ForeignKey(Codigo_Descuento, null=True, blank=True)
    fecha = models.DateTimeField(auto_now=True)


def authorize(request, context):
    if 'auth_comercio' in request.COOKIES:
        comercio = Comercio.objects.get(id=int(decrypt_val(request.COOKIES['auth_comercio'])))
        context['auth_comercio'] = comercio
        context['aut_nombre'] = comercio.nombre
    if 'auth_usuario' in request.COOKIES:
        usuario = Usuario.objects.get(id=int(decrypt_val(request.COOKIES['auth_usuario'])))
        context['auth_usuario'] = usuario
        context['aut_nombre'] = "%s %s" % (usuario.nombre, usuario.apellido)
    if 'auth_empleado' in request.COOKIES:
        empleado = Empleado.objects.get(id=int(decrypt_val(request.COOKIES['auth_empleado'])))
        context['auth_empleado'] = empleado
        context['aut_nombre'] = "%s %s" % (empleado.nombre, empleado.apellido)
    return context
