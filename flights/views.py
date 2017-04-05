from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import Flights, ActiveFlights

def index(request):
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

def flightdetail(request, just_date, callsign, cid):
    req_flight = Flights.objects.get(just_date = just_date, callsign = callsign, cid = cid)
    altitude_array = req_flight.get_altitude_array();
    context = {
        'req_flight': req_flight,
        'alti_array': altitude_array
    }
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


def altitude(request, just_date, callsign, cid):
    req_flight = Flights.objects.get(just_date = just_date, callsign = callsign, cid = cid)
    altitude_array = req_flight.get_altitude_array();
    data = []
    for i, alt in enumerate(altitude_array):
        obj = {
            'index': i,
            'altitude': alt
        }
        data.append(obj)
    return JsonResponse(data, safe=False)

'''
def altitude(request):
    return HttpResponse("Yo, this is the index for flights.")
'''
