from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from .views import *


urlpatterns = [
    #url(r'^$', index_app, name='arca'),
    url(r'^comercios/', index_comercio, name='arca_comercios'),
    url(r'^login_app/', login_app, name='arca_login_app'),
    url(r'^login_comercio/', login_comercio.as_view(), name='arca_login_comercio'),
    url(r'^logout_comercio/', logout_comercio, name='arca_logout_comercio'),



    url(r'^$', Index.as_view(), name='arca_index'),
    url(r'^login/', Login.as_view(), name='arca_login'),
    url(r'^get_comercio_categorias/', get_comercio_categorias, name="get_comercio_categorias"),
    url(r'^account_profile/',
        login_required(function=account_profile.as_view(),
                       login_url="arca_login"), name="account_profile"),

    url(r'^registrar_negocio/',registrar_negocio.as_view(), name="registrar_negocio"),

    url(r'^registrar_negocio_st1/', registrar_negocio_st1.as_view(), name="registrar_negocio_st1"),
    url(r'^registrar_negocio_st2/', registrar_negocio_st2.as_view(), name="registrar_negocio_st2"),
    url(r'^registrar_negocio_st3/', registrar_negocio_st3.as_view(), name="registrar_negocio_st3"),
    url(r'^registrar_negocio_st4/', registrar_negocio_st4.as_view(), name="registrar_negocio_st4"),

    url(r'^mi_comercio/', mi_comercio.as_view(), name="mi_comercio"),
    url(r'^edit_comercio/', edit_comercio.as_view(), name="edit_comercio"),

    url(r'^render_descuento/', render_descuento, name="render_descuento"),
    url(r'^render_listado_descuento/', render_listado_descuento, name="render_listado_descuento"),
    url(r'^save_descuento/', save_descuento, name="save_descuento"),
    url(r'^render_listado_cupones/', render_listado_cupones, name="render_listado_cupones"),
    url(r'^render_cupon/', render_cupon, name="render_cupon"),
    url(r'^save_cupon/', save_cupon,  name="save_cupon"),

    url(r'^render_listado_empleado/', render_listado_empleado, name="render_listado_empleado"),
    url(r'^render_empleado/', render_empleado, name="render_empleado"),
    url(r'^save_empleado/', save_empleado, name="save_empleado"),

    url(r'^dashboard_comercio/', dashboard_comercio.as_view(), name="dashboard_comercio"),
]
