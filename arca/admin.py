from arca.models import *
from django.contrib import admin

# Register your models here.
admin.site.register(Comercio_Categoria)
admin.site.register(Empleado)

class comercio_admin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'propietario')

admin.site.register(Comercio, comercio_admin)
