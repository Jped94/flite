from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.active, name = 'active'),
    url(r'^api/altitude/(?P<callsign>[0-9a-zA-Z]{3,7})(?P<just_date>[0-9]{4}[-]{1}[0-9]{2}[-]{1}[0-9]{2})(?P<cid>[0-9a-zA-Z]{5,8})/$', views.altitude, name = 'altitude'),
    #url(r'^api/altitude', views.altitude, name = 'altitude'),
    url(r'^(?P<callsign>[0-9a-zA-Z]{3,7})(?P<just_date>[0-9]{4}[-]{1}[0-9]{2}[-]{1}[0-9]{2})(?P<cid>[0-9a-zA-Z]{5,8})/$', views.flightdetail, name='flightdetail'),
]
