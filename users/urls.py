from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<cid>[0-9]+)/$', views.user_info, name='user_info'),
]
