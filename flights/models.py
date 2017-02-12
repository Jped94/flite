from __future__ import unicode_literals

from django.db import models

class ActiveFlights(models.Model):
	datetime = models.DateTimeField()
	callsign = models.CharField(max_length=10)
	cid = models.CharField(max_length=30)
	clienttype = models.CharField(max_length=10)
	latitude = models.DecimalField(max_digits=8, decimal_places=6)
	longitude = models.DecimalField(max_digits=9, decimal_places=6)
	server = models.CharField(max_length=15)
	altitude = models.IntegerField()
	groundspeed = models.IntegerField()
	transponder = models.IntegerField()
	heading = models.IntegerField()
	flight_status = models.CharField(max_length=20)
	class Meta:
		unique_together = ("datetime", "callsign", "cid")

	def __str__(self):
		return str(self.datetime) + self.callsign + self.cid


'''class ActiveControllers(models.Model):
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

	class Meta:
		unique_together = ("datetime", "callsign", "cid")

	def __str__(self):
		return str(self.datetime) + self.callsign + self.cid
'''

class Flights(models.Model):
	#autonumber
	just_date = models.DateField()
	callsign = models.CharField(max_length=10)
	cid = models.CharField(max_length=30)
	planned_aircraft = models.CharField(max_length=8)
	planned_tascruise = models.IntegerField()
	planned_depairport = models.CharField(max_length=4)
	planned_altitude = models.IntegerField()
	planned_destairport = models.CharField(max_length=4)
	planned_deptime = models.TimeField(null=True)
	planned_actdeptime = models.TimeField(null=True)
	planned_altairport = models.CharField(max_length=4)
	planned_remarks = models.CharField(max_length=255)
	planned_route = models.TextField()
	time_logon = models.DateTimeField(null = True)
	Routestring = models.TextField()
	duration = models.TimeField()
	total_distance = models.IntegerField()
	day_night = models.CharField(max_length=1) #0=day, 1=night
	outRamp = models.DateTimeField(null = True)
	offGround = models.DateTimeField(null = True)
	onGround = models.DateTimeField(null = True)
	inGate = models.DateTimeField(null = True)
	groundTime = models.FloatField(null = True)
	altitudeString = models.TextField()
	class Meta:
		unique_together = ("just_date", "callsign", "cid")

	def __str__(self):
		return str(self.just_date) + self.callsign + self.cid

class Aircrafts(models.Model):
	id = models.IntegerField(primary_key=True)
	aircraft_type = models.CharField(max_length=1)
	mfgr = models.CharField(max_length=30)
	model = models.CharField(max_length=30)
	code = models.CharField(max_length=4)
	engineqty = models.IntegerField()
	enginetype = models.CharField(max_length=1)
	weightclass = models.CharField(max_length=1)
	descentrate = models.CharField(max_length=10)
	serviceceiling = models.CharField(max_length=10)
	cruisetas = models.CharField(max_length=10)
	def __str__(self):
		return self.id

class Airlines(models.Model):
	id = models.IntegerField(primary_key=True)
	icao = models.CharField(max_length=10, unique=True)
	name = models.CharField(max_length=100)
	radio = models.CharField(max_length=100, null=True)
	website = models.CharField(max_length=100, null=True)
	def __str__(self):
		return self.id

class Airports(models.Model):
	id = models.IntegerField(primary_key=True)
	icao = models.CharField(max_length=10, unique=True)
	name = models.CharField(max_length=100)
	lat = models.DecimalField(max_digits=9, decimal_places=6)
	lon = models.DecimalField(max_digits=10, decimal_places=6)
	alt = models.IntegerField(null=True)
	iata = models.CharField(max_length=4, null=True)
	city = models.CharField(max_length=50, null=True)
	iso = models.CharField(max_length=2)
	FIR = models.CharField(max_length=4, null=True)
	def __str__(self):
		return self.name

class Isocodes(models.Model):
	code = models.CharField(max_length=2, primary_key=True)
	country = models.CharField(max_length=100)
	cleaned = models.IntegerField()
	def __str__(self):
		return self.code

class Registrations(models.Model):
	id = models.IntegerField(primary_key=True)
	prefix = models.CharField(max_length=5)
	iso = models.CharField(max_length=2, null=True)
	def __str__(self):
		return self.id
