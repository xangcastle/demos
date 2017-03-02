from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin


class base_tabular(admin.TabularInline):
    extra = 0
    classes = ('grp-collapse grp-open',)

class Tipo_Contacto_admin(admin.ModelAdmin):
    list_display = ("tipo", "icono")
    list_filter = ("tipo", "icono")
    search_fields = ("tipo", "icono")

admin.site.register(Tipo_Contacto, Tipo_Contacto_admin)

class propietario_contacto(base_tabular):
    model = Propietario_Contacto
    verbose_name = "Contacto"
    verbose_name_plural = "Datos de contacto"
    fields = ('tipo_contacto', 'valor')


    def get_actions(self, request):
        actions = super(propietario_contacto, self).get_actions(request)
        del actions['export_as_xls']
        return actions

class Propietario_admin(admin.ModelAdmin):
    list_display = ("nombre", "apellido", "razon_social")
    list_filter = ("nombre", "apellido", "razon_social")
    search_fields = ("nombre", "apellido", "razon_social")
    fieldsets = (
        ('Datos Generales', {
            'classes': ('grp-collapse grp-open',),
            'fields': (
                ('nombre', 'apellido',),
                ('razon_social'),
                ('is_corporative',)
            ),
        }),
    )
    inlines = [propietario_contacto]

admin.site.register(Propietario, Propietario_admin)

class propiedad_galeria(base_tabular):
    model = Foto
    verbose_name = "Foto"
    verbose_name_plural = "Galeria de imagenes"

class propiedad_extras(base_tabular):
    model = Propiedad_Extra
    verbose_name = "Propiedad"
    verbose_name_plural = "Detalles Adicionales"

class Propiedad_admin(admin.ModelAdmin):
    list_display = ("propietario", "habitaciones", "localidad", "direccion")
    list_filter = ("propietario", "habitaciones", "localidad", "direccion")
    search_fields = ("propietario", "habitaciones", "localidad", "direccion")
    fieldsets = (
        ('Datos Generales', {
            'classes': ('grp-collapse grp-open',),
            'fields': (
                ('nombre', 'propietario',),
                ('area','habitaciones','banios',),
                ('cochera','plantas', 'pisina',),
                ('portada', 'localidad'),
                ('estado_negocio','valor'),
                ('direccion'),
                ('descripcion'),
                ('position'),
            ),
        }),
    )
    inlines = [propiedad_galeria, propiedad_extras]
    verbose_name = "Propiedades"
    verbose_name_plural = "Propiedades"

admin.site.register(Propiedad, Propiedad_admin)

admin.site.register(Departamento)
admin.site.register(Municipio)
admin.site.register(Localidad)
