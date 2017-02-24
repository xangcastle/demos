from __future__ import unicode_literals

from colorfield.fields import ColorField
from django.conf import settings
from django.db import models


def get_aplications(user):
    ids = []
    for a in Aplicacion.objects.all():
        if user.has_perm('control.' + a.name):
            ids.append(a.id)
    apps = Aplicacion.objects.filter(id__in=ids).order_by('id')
    return apps


def get_options(user):
    try:
        return Opcion.objects.get(user=user)
    except:
        return Opcion(user=user)

def get_permission():
    perms = []
    for a in Aplicacion.objects.all():
        perms.append((a.name, "Can use " + a.name))
    return tuple(perms)


class Opcion(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    background = models.ImageField(upload_to="fondos", null=True, blank=True)


class Aplicacion(models.Model):
    name = models.CharField(max_length=25, null=True, verbose_name="nombre de la aplicacion")
    label = models.CharField(max_length=25, blank=True, null=True, verbose_name="etiqueta de la aplicacion")
    icono = models.ImageField(upload_to="iconos", null=True, blank=True)
    background_color = ColorField(default='#FF0000')


    class Meta:
        verbose_name_plural = "aplicaciones"

    def __unicode__(self):
        return self.name



class Permiso(models.Model):
    class Meta:
        #pass
        permissions = get_permission()
