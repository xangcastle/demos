"""demos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from inblensa.views import index, suck
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', login_required(index.as_view()), name="control_index"),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^inblensa/', include("inblensa.urls")),
    url(r'^realstate/', include("realstate.urls")),
    url(r'^ajax/', include('inblensa.ajax_urls')),
    url(r'^app/execute_import_cliente/', suck),
    url(r'^rrhh/', include("rrhh.urls")),
    url(r'^soc/', include("social_django.urls", namespace="social")),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^johnmay/', include('johnmay.urls'), ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
