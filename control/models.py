from __future__ import unicode_literals

from colorfield.fields import ColorField
from django.conf import settings
from django.db import models
from django.utils.safestring import mark_safe


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

    def __unicode__(self):
        return self.user.username


class Aplicacion(models.Model):
    name = models.CharField(max_length=25, null=True, verbose_name="nombre de la aplicacion")
    label = models.CharField(max_length=25, blank=True, null=True, verbose_name="etiqueta de la aplicacion")
    icono = models.ImageField(upload_to="iconos", null=True, blank=True)
    background_color = ColorField(default='#FF0000')


    class Meta:
        verbose_name_plural = "aplicaciones"

    def __unicode__(self):
        return self.name

    def image_tag(self):
        return mark_safe('<div style="height: 100px; width: 100px; text-align: center; border-radius: 15px;'
                         'background: linear-gradient(%s, rgba(34, 34, 34, 0.12));" >'
                         '<img src="/media/%s" width="80px" height="80px" '
                         'style="display: table-cell;     vertical-align: middle; text-align: center; padding: 10px;"/>'
                         '</div>' % (self.background_color, self.icono))

    image_tag.short_description = 'Image'

    def background_tag(self):
        return mark_safe('<div style="height: 30px; width: 100px; '
                         'background: linear-gradient(%s, rgba(34, 34, 34, 0.12));" />' % (self.background_color))

    background_tag.short_description = 'Fondo'



class Permiso(models.Model):
    class Meta:
        pass
        #permissions = get_permission()
