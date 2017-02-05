from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Flights

def index(request):
    return HttpResponse("Yo, this is the index for flights.")

def flightdetail(request, just_date, callsign, cid):
    req_flight = Flights.objects.get(just_date = just_date, callsign = callsign, cid = cid)
    context = {'req_flight': req_flight}
    return render (request, 'flights/flightdetail.html', context)
# Create your views here.
