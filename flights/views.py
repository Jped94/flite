from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Flights, ActiveFlights

def index(request):
    return HttpResponse("Yo, this is the index for flights.")

def flightdetail(request, just_date, callsign, cid):
    req_flight = Flights.objects.get(just_date = just_date, callsign = callsign, cid = cid)
    context = {'req_flight': req_flight}
    return render (request, 'flights/flightdetail.html', context)

def active(request):
    plain_actives = ActiveFlights.objects.order_by('-datetime')
    actives = []
    for flight in plain_actives:
        assoc_flight = Flights.objects.get(id = flight.flight_id)
        new_obj = {
            'active': flight,
            'flight': assoc_flight
        }
        actives.append(new_obj)

    context = {'actives': actives}
    return render(request, 'flights/active.html', context)


# Create your views here.
