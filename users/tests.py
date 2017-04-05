from django.test import TestCase

import datetime
from django.utils import timezone
from django.test import TestCase
from django.db import models
from flights.models import Flights
from .models import Personal
# Create your tests here.
class UserMethodTests(TestCase):

    def test_get_avg_ground_time_with_one_flight(self):
        '''
        Should just return the groundtime for the one flight
        '''
        timenow = timezone.datetime.now().time()
        datenow = datetime.datetime.now()
        test_personal = Personal(
                            cid = "123456",
                        	realname = "Joshua Pedowitz",
                        	pilot_rating = "Pilot",
                        	atc_rating = "atc"
                            )
        test_personal.save()
        
        test_flight = Flights(
                            just_date = datetime.datetime.now().date(),
                            callsign = "stoopid",
                        	cid = "123456",
                        	planned_aircraft = "sdfsd",
                        	planned_tascruise = 500,
                        	planned_depairport = "KHPN",
                        	planned_altitude = 30000,
                        	planned_destairport = "KFJK",
                        	planned_deptime = timenow,
                        	planned_actdeptime = timenow,
                        	planned_altairport = "KLAX",
                        	planned_remarks = "this is a test",
                        	planned_route = "sdfsdlkfjslkdfjlkfjkdfjkfdjkfdjksdfjklsjlfkdjlskdf",
                        	time_logon = datenow,
                        	Routestring = "12.12343,234.4567;12.12343,234.4567;12.12343,234.4567;12.12343,234.4567;12.12343,234.4567;12.12343,234.4567;12.12343,234.4567;",
                        	duration = timenow,
                        	total_distance = 34534,
                        	day_night = "0", #0=day, 1=night
                        	outRamp = datetime.datetime.now(),
                        	offGround = datetime.datetime.now(),
                        	onGround = datetime.datetime.now(),
                        	inGate = datetime.datetime.now(),
                        	groundTime = 1000.0,
                        	altitudeString = "12;13;25;667;356;3545;5677;10000;15000;20000;25000;30000;"
                            )
        test_flight.save()

        self.assertEqual(test_personal.get_avg_ground_time(), 1000.0)
