from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from users.models import Personal
from flights.models import Flights, ActiveFlights


# Create your views here.

def index(request):
    user_objs = Personal.objects.order_by('-cid')[:30]
    actives = ActiveFlights.objects.all()
    numOnline = actives.count()
    template = loader.get_template('users/index.html')
    context = {
        'user_objs': user_objs,
        'actives': actives,
        'numOnline': numOnline
    }
    return HttpResponse(template.render(context, request))

def user_info(request, cid):
    user_obj = Personal.objects.get(cid = cid)
    #flights_list = Flights.objects.filter(cid = cid) #.order_by('-just_date')
    flights_list = user_obj.get_associated_flights()
    ground_time = user_obj.get_avg_ground_time()
    template = loader.get_template('users/user.html')
    context = {
        'user_obj': user_obj,
        'flights_list': flights_list,
        'gt': ground_time
    }
    return HttpResponse(template.render(context, request))
