from django.conf.urls import include, url


from .views import *
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [
    url(r'^$', Index.as_view(), name='arca_index'),
    url(r'^login/', Login.as_view(), name='arca_login'),
    url(r'^get_comercio_categorias/', get_comercio_categorias, name="get_comercio_categorias"),
    url(r'^account_profile/',
        login_required(function= account_profile.as_view(),
                       login_url="arca_login"), name="account_profile"),
    url(r'^registrar_negocio/',
        login_required(function=registrar_negocio.as_view(),
                       login_url="arca_login"), name="registrar_negocio"),
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
