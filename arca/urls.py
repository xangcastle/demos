from django.conf.urls import include, url


from .views import *
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [
    url(r'^$', Index.as_view(), name='arca_index'),
    url(r'^$', Login.as_view(), name='arca_login'),
]
