from django.contrib import admin
from .models import *


class empleado_admin(admin.ModelAdmin):
    list_display = ('nombre', 'cedula', 'inss', 'salario')
    search_fields = ('nombre', 'cedula', 'inss')
admin.site.register(Empleado, empleado_admin)

class pago_empleados(admin.TabularInline):
    model = PagoEmpleado
    extra = 0

class planilla_admin(admin.ModelAdmin):
    change_form_template = "rrhh/planilla.html"
    date_hierarchy = 'fecha_fin'
    fields = (('fecha_inicio', 'fecha_fin'), )
    inlines = [pago_empleados, ]
    ordering = []
admin.site.register(Planilla, planilla_admin)
