from arca.models import *
from django.contrib import admin

admin.site.register(Usuario)
admin.site.register(Comercio_Categoria)
class ComercioAdmin(admin.ModelAdmin):
    list_display = ('thumbnai', 'nombre', 'direccion')
    fields = (('username', 'password'), ('nombre', 'nombre_propietario'), 'direccion',
              'identificacion', ('logo', 'baner'), 'tiene_descuento_vigencia',
              'tiene_descuento_compra_minima', 'tiene_servicio_afiliacion',
              'tiene_servicio_crm')
    readonly_fields = ('password', )
    actions = ['action_restablecer_password', ]

    def action_restablecer_password(self, request, queryset):
        if 'apply' in request:
            for o in queryset:
                o.restablecer_password(request.POST.get('password', ''))
            return None
        return None


admin.site.register(Comercio, ComercioAdmin)
admin.site.register(Empleado)
admin.site.register(Descuento)
admin.site.register(Codigo_Descuento)
admin.site.register(Publicidad)
admin.site.register(Producto)
