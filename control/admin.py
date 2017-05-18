from django.contrib import admin
from .models import *

class Aplication_Page_Admin(admin.ModelAdmin):
    list_display = ('name', 'image_tag')
    fields = ('name', 'icono', 'background_color')

class RegistroAdmin(admin.ModelAdmin):
    list_display = ('tag', 'usuario', 'fecha')

admin.site.register(Aplicacion,Aplication_Page_Admin)

admin.site.register(Opcion)

admin.site.register(Registro, RegistroAdmin)