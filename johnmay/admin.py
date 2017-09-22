from django.contrib import admin
from .models import *

class Bodega(admin.AdminSite):
    site_title = "Johnmay Bodega"



bodega = Bodega(name='bodega')


admin.site.register(Perfil)
admin.site.register(Marca)
admin.site.register(Categoria)


class BodegaExistencias(admin.TabularInline):
    model = Existencia
    readonly_fields = ('bodega', 'cantidad', 'precio_pactado')
    extra = 0


class BodegaProducto(admin.ModelAdmin):
    inlines = [BodegaExistencias, ]

bodega.register(Producto, BodegaProducto)
bodega.register(Documento)


