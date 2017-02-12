from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from users.models import Personal
from flights.models import Flights


# Create your views here.

def index(request):
    user_objs = Personal.objects.order_by('-cid')[:30]
    template = loader.get_template('users/index.html')
    context = {
        'user_objs': user_objs,
    }
    return HttpResponse(template.render(context, request))

def user_info(request, cid):
    user_obj = Personal.objects.get(cid = cid)
    flights_list = Flights.objects.filter(cid = cid) #.order_by('-just_date')
    template = loader.get_template('users/user.html')
    context = {
        'user_obj': user_obj,
        'flights_list': flights_list
    }
    return HttpResponse(template.render(context, request))
