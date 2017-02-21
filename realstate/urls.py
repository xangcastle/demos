from django.conf.urls import include, url

from django.contrib.auth.decorators import login_required
from realstate.views import *

urlpatterns = [
    url(r'^$', index.as_view(), name='index'),
    url(r'^get_usuario/', get_usuario, name='get_usuario'),
    url(r'^get_propiedades/', get_propiedades.as_view(), name='get_propiedades'),
    url(r'^get_propiedad/', get_propiedad, name="get_propiedad"),
    url(r'^get_foto_propiedad/', get_foto_propiedad, name="get_foto_propiedad"),
    url(r'^get_propietario/', get_propietario, name="get_propietario"),
    url(r'^property/', show_propiedad.as_view(), name="propiedad"),
    url(r'^send_mail/', enviar_mail.as_view(), name="enviar_email"),
]