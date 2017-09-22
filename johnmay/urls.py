from django.conf.urls import url, include
from .admin import bodega

urlpatterns = [
    url(r'bodega/', include(bodega.urls), name='johnmay_bodega'),
]
