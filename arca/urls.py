from django.conf.urls import include, url


from .views import *
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [
    url(r'^$', login_required(Index.as_view()), name='arca_index'),
]
