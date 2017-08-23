from __future__ import unicode_literals

from django.db import models
from django.forms import model_to_dict
from datetime import datetime
import calendar
from django.contrib.auth.models import User, UserManager
from .base import Base
from django.db.models.functions import Length
from django.db.models.signals import post_save
from django.dispatch import receiver
from .base import Base
from django.db.models import Avg
from django.db.models.functions import Coalesce

CALIFICACIONES = (
                   (1,'MALO'),
                   (2,'REGULAR'),
                   (3,'ACEPTABLE'),
                   (4,'BUENO'),
                   (5,'EXCELENTE')
                  )

ESTADO_PEDIDO  = (
                   (1,'PAGADO'),
                   (2,'ENVIADO'),
                   (3,'RECHAZADO'),
                   (4,'EN REPARTO'),
                   (5,'ENTREGADO')
                  )
TIPO_ORDEN      = (
                     (1,'CARRO DE COMPRAS'),
                     (2,'ORDEN')
                  )

ESTADO_PRODUCTO  = (
                       (1,'PENDIENTE'),
                       (2,'EN VERIFICACION'),
                       (3,'PUBLICADO'),
                       (4,'DESHABILITADO')
                  )

class TC(Base):
    fecha = models.DateField()
    tc = models.FloatField()

class Pais(Base):
    nombre    = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class Departamento(Base):
    nombre    = models.CharField(max_length=200)
    pais      = models.ForeignKey(Pais, null=True, blank=True)

    def __str__(self):
        return self.nombre

class Municipio(Base):
    nombre       = models.CharField(max_length=200)
    departamento = models.ForeignKey(Departamento, null=True, blank=True)
    def __str__(self):
        return  self.nombre

class Barrio(Base):
    nombre    = models.CharField(max_length=200)
    municipio = models.ForeignKey(Municipio, null=True, blank=True)
    def __str__(self):
        return self.nombre

class Cliente(Base):
    pais         = models.ForeignKey(Pais, null=True, blank=True)
    departamento = models.ForeignKey(Departamento, null=True, blank=True)
    municipio    = models.ForeignKey(Municipio, null=True, blank=True)
    barrio       = models.ForeignKey(Barrio, null=True, blank=True)
    direccion    = models.CharField(max_length=400)
    telefono     = models.CharField(max_length=12)
    suscrito     = models.BooleanField(default=False)
    user         = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def listaDeDeseos(self):
        return ListaDeseo.objects.filter(cliente=self)

    def carritoCompra(self):
        return Orden.objects.get(cliente=self,tipo=1)

    def totalCompra(self):
        total  = 0.0
        for item in self.carritoCompra().productos():
            total += item.totalProducto()
        return total

class Proveedor(Base):
    telefono     = models.CharField(max_length=30)
    provincia    = models.CharField(max_length=100)
    ciudad       = models.CharField(max_length=100)
    distrito     = models.CharField(max_length=100)
    direccion    = models.CharField(max_length=100)
    user         = models.OneToOneField(User, on_delete=models.CASCADE)
    #objects      = models.Manager() # cliente.objects.filter()
    #objects      = UserManager() # trae create(username, email, password)
    def __str__(self):
        return self.user.username

    """@receiver(post_save, sender=User)
    def create_user_proveedor(sender, instance, created, **kwargs):
        if created:
            Proveedor.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_proveedor(sender, instance, **kwargs):
        instance.proveedor.save()"""

class Categoria(Base):
    codigo = models.CharField(max_length=65)
    nombre = models.CharField(max_length=255)
    imagen = models.ImageField(upload_to="categorias", null=True, blank=True)
    padre  = models.ForeignKey('self', null=True, blank=True, related_name="%(app_label)s_%(class)s_padre")
    def __str__(self):
        return '%s %s' % (self.codigo, self.nombre)

class ProductoManager(models.Manager):
    def get_by_natural_key(self, nombre,id,precio_venta,imagen):
        return self.get(nombre=nombre, id=id,precio_venta=precio_venta,imagen=imagen.url)

class Producto(Base):
    objects               = ProductoManager()
    nombre                = models.CharField(max_length=200)
    precio_proveedor      = models.FloatField(default=0.0)
    precio_venta          = models.FloatField(default=0.0)
    precio_anterior_venta = models.FloatField(default=0.0)
    proveedor             = models.ForeignKey(Proveedor, null=True, blank=True)
    categoria             = models.ForeignKey(Categoria, null=True, blank=True)
    descripcion           = models.CharField(max_length=500)
    caracteristicasTecnica= models.CharField(max_length=10000)
    imagen                = models.ImageField(upload_to="productos")
    modelo                = models.CharField(max_length=200)
    estado                = models.IntegerField(choices=ESTADO_PRODUCTO)
    fecha_creacion        = models.DateField(default=datetime.now, blank=True)
    plantilla             = models.CharField(max_length=500,default='home/product2.html')
    tipo                  = models.IntegerField(null=True, blank=True)

    def costoTotal(self):
      return self.precio_venta

    def materiales(self):
      return  Material.objects.filter(producto=self)

    def __str__(self):
        return self.nombre

    def reviews(self):
        return Review.objects.filter(producto=self)

    def puntuacion(self):
        return round(self.reviews().aggregate(puntuacion = Coalesce(Avg('calificacion'),0.0))['puntuacion'], 2)

    def multimedia(self):
        return Multimedia.objects.filter(producto=self)

    def natural_key(self):
        return (self.nombre, self.id,self.precio_venta,self.imagen.url)

    class Meta:
        unique_together = (('nombre', 'id','precio_venta','imagen'),)



class Material(Base):
      nombre                 = models.CharField(max_length=60)
      imagen                 = models.ImageField(upload_to="materiales")
      costoMetroProveedor    = models.FloatField(default=0.0)
      costoMetroVenta        = models.FloatField(default=0.0)
      producto               = models.ForeignKey(Producto)

class CaracteristasEspecial(models.Model):
    ancho                 = models.FloatField(default=0.0)
    alto                  = models.FloatField(default=0.0)
    precio                = models.FloatField(default=0.0)
    material              = models.ForeignKey(Material, null=True, blank=True)


class Multimedia(Base):
    archivo     = models.FileField(upload_to="productos")
    ancho       = models.FloatField(default=0.0)
    alto        = models.FloatField(default=0.0)
    producto    = models.ForeignKey(Producto, null=True, blank=True)
    tipo        = models.CharField(max_length=2, choices=(('vi', 'VIDEO'), ('im', 'FOTO')), default='im')

class Review(Base):
    producto     = models.ForeignKey(Producto)
    calificacion = models.FloatField(choices=CALIFICACIONES)
    comentario   = models.CharField(max_length=500)
    cliente      = models.ForeignKey(Cliente, null=True, blank=True)

class Orden(Base):
    fecha_pedido               = models.DateField(null=True, blank=True)
    fecha_entrega              = models.DateField(null=True, blank=True)
    fecha_transaccion_bancaria = models.DateField(null=True, blank=True)
    precio_total               = models.FloatField(default=0.0)
    cliente                    = models.ForeignKey(Cliente)
    comentario                 = models.CharField(max_length=500,null=True, blank=True)
    calificacion               = models.IntegerField(choices=CALIFICACIONES,null=True, blank=True)
    tipo                       = models.IntegerField(choices=TIPO_ORDEN)

    def productos(self):
        return ProductoPedido.objects.filter(orden=self)

    def estados(self):
        return EstadosOrdenes.objects.filter(orden=self)


class EstadosOrdenes(Base):
      tipo        = models.IntegerField(choices=ESTADO_PEDIDO)
      imagen      = models.ImageField(upload_to="ordenes",null=True, blank=True)
      descripcion = models.CharField(max_length=500,null=True, blank=True)
      fecha       = models.DateField()


class ProductoPedido(Base):
    producto                 = models.ForeignKey(Producto)
    orden                    = models.ForeignKey(Orden)
    calificacion             = models.IntegerField(choices=CALIFICACIONES,null=True, blank=True)
    comentario               = models.CharField(max_length=500,null=True, blank=True)
    caracteristas_especiales = models.ForeignKey(CaracteristasEspecial,null=True, blank=True)
    cantidad                 = models.PositiveSmallIntegerField(default=0)

    def natural_key(self):
         return (self.cantidad,) + self.producto.natural_key()
    def totalProducto(self):
         total = 0.0
         if self.caracteristas_especiales :
             total =  self.caracteristas_especiales.precio * self.cantidad
         else :
             total =  self.producto.precio_venta * self.cantidad
         return total

class ListaDeseo(Base):
    cliente      = models.ForeignKey(Cliente, null=True, blank=True)
    producto     = models.ForeignKey(Producto)
    def productos(self):
        return ProductoLista.objects.filter(lista=self)
