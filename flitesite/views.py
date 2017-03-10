from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from users.models import Personal
from flights.models import Flights


# Create your views here.

def homeindex(request):
    user_objs = Personal.objects.order_by('-cid')[:30]
    template = loader.get_template('flitesite/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

def flight_data(request):
    data = Flights.objects.all()
    return JsonResponse(list(data), safe=False)
