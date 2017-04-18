from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from flights.models import Flights
import pandas as pd
import numpy as np

class Personal(models.Model):
	cid = models.CharField(max_length=30, primary_key=True)
	realname = models.CharField(max_length=50)
	pilot_rating = models.CharField(max_length=30)
	atc_rating = models.CharField(max_length=30)
	def __str__(self):
		return self.realname

	def get_associated_flights(self):
		assoc_flights = Flights.objects.filter(cid=self.cid)
		return assoc_flights

	def get_avg_ground_time(self):
		flights = Flights.objects.filter(cid=self.cid)
		flights = pd.DataFrame.from_records(flights.values())
		flights = flights[(flights['groundTime'].notnull())]
		return flights['groundTime'].mean()

	def get_most_common_airport(self):

		def airportPair(x): #Helper function for commonAirport
		#having issues here
			print x
		'''
			if (x[12] < x[14]):
				return (x[12], x[14])
			else:
				return (x[14], x[12])
		'''

		flights = Flights.objects.filter(cid=self.cid)
		flights = pd.DataFrame.from_records(flights.values())
		airportpairs = flights[(flights['planned_depairport'] != '') & (flights['planned_destairport'] != '')]


		x = airportpairs.apply(airportPair, axis=1).mode()
		#airports here should be a query to get all airports
		a = airports[(airports['icao'] == x[0][0])]
		b = airports[(airports['icao'] == x[0][1])]

		ports_obj = {
			'airport1': a,
			'airport2': b
		}

		return ports_obj



class ActiveControllers(models.Model):
	datetime = models.DateTimeField()
	callsign = models.CharField(max_length=10)
	cid = models.CharField(max_length=30)
	clienttype = models.CharField(max_length=10)
	frequency = models.DecimalField(max_digits=6, decimal_places=3)
	latitude = models.DecimalField(max_digits=8, decimal_places=6)
	longitude = models.DecimalField(max_digits=9, decimal_places=6)
	server = models.CharField(max_length=15)
	facilitytype = models.CharField(max_length=30)
	visualrange = models.IntegerField()
	time_logon = models.DateTimeField()

	def __str__(self):
		return str(self.datetime) + self.callsign + self.cid
	class Meta:
		unique_together = ("datetime", "callsign", "cid")

class Controllers(models.Model):
	date = models.DateField()
	callsign = models.CharField(max_length=10)
	cid = models.CharField(max_length=30, primary_key = True)
	facilitytype = models.CharField(max_length=1)
	TotalTime = models.TimeField()
	lastUpdate = models.DateTimeField()

	def __str__(self):
		return self.cid
