from arca.models import *
from django.contrib import admin
from arca.crypter import decrypt_val, encrypt_val
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django import forms
from django.template.context_processors import csrf

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

    class PasswordForm(forms.Form):
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        password = forms.CharField(max_length=65, widget=forms.PasswordInput)
        confirm = forms.CharField(max_length=65, widget=forms.PasswordInput)

        def clean_confirm(self):
            password = self.cleaned_data['password']
            confirm = self.cleaned_data['confirm']
            if not (password == confirm):
                raise forms.ValidationError("Los campos no coiciden!")
            return confirm

    def action_restablecer_password(self, request, queryset):
        message = ""
        form = None
        if 'apply' in request.POST:
            form = self.PasswordForm(request.POST)
            if form.is_valid():
                message = "Se ha restablecido el password de los comercios seleccionados"
                password = form.cleaned_data['password']
                queryset.update(password=encrypt_val(password))
            self.message_user(request, message)
            return HttpResponseRedirect(request.get_full_path())

        if not form:
            form = self.PasswordForm(
                initial={
                    '_selected_action': request.POST.getlist(
                        admin.ACTION_CHECKBOX_NAME)})

        data = {'queryset': queryset, 'form': form,
                'header_tittle': 'Por favor rellene todos los campos',
                'explanation':
                    'Se restablecera el password para los siguientes comercios:',
                'action': 'action_restablecer_password'}
        self.message_user(request, message)
        data.update(csrf(request))
        return render_to_response('admin/RestablecerPassword.html', data)


    action_restablecer_password.short_description = "Restablecer Password"


admin.site.register(Comercio, ComercioAdmin)
admin.site.register(Empleado)
admin.site.register(Descuento)
admin.site.register(Codigo_Descuento)
admin.site.register(Publicidad)
admin.site.register(Producto)
