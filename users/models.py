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
