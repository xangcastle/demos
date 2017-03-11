from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from .views import *


urlpatterns = [
    #url(r'^$', index_app, name='arca'),
    url(r'^comercios/', index_comercio, name='arca_comercios'),
    url(r'^login_app/', login_app, name='arca_login_app'),
    url(r'^login_comercio/', login_comercio.as_view(), name='arca_login_comercio'),

    url(r'^$', Index.as_view(), name='arca_index'),
    url(r'^login/', Login.as_view(), name='arca_login'),
    url(r'^get_comercio_categorias/', get_comercio_categorias, name="get_comercio_categorias"),
    url(r'^account_profile/',
        login_required(function=account_profile.as_view(),
                       login_url="arca_login"), name="account_profile"),

    url(r'^registrar_negocio/',
        login_required(function=registrar_negocio.as_view(),
                       login_url="arca_login"), name="registrar_negocio"),

    url(r'^registrar_negocio_st1/', registrar_negocio_st1.as_view(), name="registrar_negocio_st1"),
    url(r'^registrar_negocio_st2/', registrar_negocio_st2.as_view(), name="registrar_negocio_st2"),
    url(r'^registrar_negocio_st3/', registrar_negocio_st3.as_view(), name="registrar_negocio_st3"),
    url(r'^registrar_negocio_st4/', registrar_negocio_st4.as_view(), name="registrar_negocio_st4"),

    url(r'^mi_comercio/',
        login_required(function=mi_comercio.as_view(),
                       login_url="arca_login"), name="mi_comercio"),
    url(r'^render_descuento/',
        login_required(function=render_descuento,
                       login_url="arca_login"), name="render_descuento"),
    url(r'^render_listado_descuento/',
        login_required(function=render_listado_descuento,
                       login_url="arca_login"), name="render_listado_descuento"),
    url(r'^save_descuento/',
        login_required(function=save_descuento,
                       login_url="arca_login"), name="save_descuento"),
    url(r'^render_listado_cupones/',
        login_required(function=render_listado_cupones,
                       login_url="arca_login"), name="render_listado_cupones"),
    url(r'^render_cupon/',
        login_required(function=render_cupon,
                       login_url="arca_login"), name="render_cupon"),
    url(r'^save_cupon/',
        login_required(function=save_cupon,
                       login_url="arca_login"), name="save_cupon"),
]
