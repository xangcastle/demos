from django.conf.urls import include, url
from .views import *


urlpatterns = [
  url(r'^$', index_app, name='arca'),
  url(r'^comercios/', index_comercio, name='arca_comercios'),
  url(r'^login_app/', login_app, name='arca_login_app'),
  url(r'^login_comercio/', login_comercio, name='arca_login_comercio'),
]
