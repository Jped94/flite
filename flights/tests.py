from django.test import TestCase

import datetime
from django.utils import timezone
from django.test import TestCase
from django.db import models
from .models import Flights

class FlightsMethodTests(TestCase):

    maxDiff = None

    def test_get_alt_array_with_flight(self):
        """
        get_alt_array should return an array with the objects containing the lat,longitude
        """
        timenow = timezone.datetime.now().time()
        datenow = datetime.datetime.now()
        test_flight = Flights(
                            just_date = datetime.datetime.now().date,
                            callsign = models.CharField(max_length=10),
                        	cid = models.CharField(max_length=30),
                        	planned_aircraft = models.CharField(max_length=8),
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
                        	day_night = 0, #0=day, 1=night
                        	outRamp = models.DateTimeField(null = True),
                        	offGround = models.DateTimeField(null = True),
                        	onGround = models.DateTimeField(null = True),
                        	inGate = models.DateTimeField(null = True),
                        	groundTime = models.FloatField(null = True),
                        	altitudeString = "12;13;25;667;356;3545;5677;10000;15000;20000;25000;30000;"
                            )
        altitude_arr = [12,13,25,667,356,3545,5677,10000,15000,20000,25000,30000]
        '''alt_obj_array = []
        for num, alt in enumerate(altitude_arr):
            newobj = {
                "alt": alt,

            }
            '''
        self.assertEqual(test_flight.get_altitude_array(), altitude_arr)


    def test_get_alt_array_with_empty_altiarray(self):
        timenow = timezone.datetime.now().time()
        datenow = datetime.datetime.now()
        test_flight = Flights(
                            just_date = datetime.datetime.now().date,
                            callsign = models.CharField(max_length=10),
                        	cid = models.CharField(max_length=30),
                        	planned_aircraft = models.CharField(max_length=8),
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
                        	day_night = 0, #0=day, 1=night
                        	outRamp = models.DateTimeField(null = True),
                        	offGround = models.DateTimeField(null = True),
                        	onGround = models.DateTimeField(null = True),
                        	inGate = models.DateTimeField(null = True),
                        	groundTime = models.FloatField(null = True),
                        	altitudeString = ""
                            )
        altitude_arr = None

        self.assertEqual(test_flight.get_altitude_array(), altitude_arr)

    def test_get_routestring_array_with_flight(self):
        """
        get_routestring_array should return an array with the objects containing the lat,longitude
        """
        timenow = timezone.datetime.now().time()
        datenow = datetime.datetime.now()
        test_flight = Flights(
                            just_date = datetime.datetime.now().date,
                            callsign = models.CharField(max_length=10),
                        	cid = models.CharField(max_length=30),
                        	planned_aircraft = models.CharField(max_length=8),
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
                        	day_night = 0, #0=day, 1=night
                        	outRamp = models.DateTimeField(null = True),
                        	offGround = models.DateTimeField(null = True),
                        	onGround = models.DateTimeField(null = True),
                        	inGate = models.DateTimeField(null = True),
                        	groundTime = models.FloatField(null = True),
                        	altitudeString = "12;13;25;667;356;3545;5677;10000;15000;20000;25000;30000;"
                            )
        rs_array = [{'lat':12.12343,'lon':234.4567},{'lat':12.12343,'lon':234.4567},{'lat':12.12343,'lon':234.4567},{'lat':12.12343,'lon':234.4567},{'lat':12.12343,'lon':234.4567},{'lat':12.12343,'lon':234.4567},{'lat':12.12343,'lon':234.4567}]
        self.assertEqual(test_flight.get_routestring_array(), rs_array)
