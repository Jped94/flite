from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),

    url(r'^(?P<just_date>[0-9\-]{10})(?P<callsign>[0-9a-zA-Z]{4})(?P<cid>[0-9a-zA-Z]+)/$', views.flightdetail, name='flightdetail'),
]
