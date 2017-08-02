from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^imprimir/', imprimir, name='caja_impresion'),
]
