import csv
import requests
import datetime
import math
import sys
from django.conf import settings
from django.core.management.base import NoArgsCommand, CommandError
from datetime import timedelta
from django.utils.timezone import utc
from flights.models import (ActiveFlights, Flights, Airports)
from users.models import (Personal, Controllers, ActiveControllers)
from decimal import Decimal
from django.db.models import F

def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
        # csv.py doesn't do Unicode; encode temporarily as UTF-8:
        csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                                dialect=dialect, **kwargs)
        for row in csv_reader:
            #decode UTF-8 back to Unicode, cell by cell:
            yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
        for line in unicode_csv_data:
            yield line.encode('utf-8')

def getNmFromLatLon(lat1, lon1, lat2, lon2):
        R = 3443.89849 # km
        theta1 = math.radians(lat1)
        theta2 = math.radians(lat2)
        dtheta = math.radians(lat2-lat1)
        dlon = math.radians(lon2-lon1)

        a = math.sin(dtheta/2) * math.sin(dtheta/2) + math.cos(theta1) * math.cos(theta2) * math.sin(dlon/2) * math.sin(dlon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        d = R * c

        return round(d)

class Command(NoArgsCommand):
    help = "Scrapes flight info from Vatsim"

    def pilotInsert(self, row, update_time):
        #just_date
        vjust_date = update_time[0:10]
        vjust_date = datetime.datetime.strptime(vjust_date, "%Y-%m-%d")
        vjust_date = vjust_date.date()

        #callsign
        vcallsign = row[0]

        #cid
        vcid = row[1]

        #planned_aircraft
        vplanned_aircraft = row[9]

    	#planned_tascruise
        if (row[10] != ''):
            vplanned_tascruise = int(row[10])
        else:
            vplanned_tascruise = 0

    	#planned_depairport
        vplanned_depairport = row[11]

    	#planned_altitude
        try:
            vplanned_altitude = int(row[12])
        except Exception, e:
            vplanned_altitude = 0

    	#planned_destairport
        vplanned_destairport = row[13]

    	#planned_deptime
        vplanned_deptime = row[22][0:2] + ":" + row[22][2:4]
        try:
            vplanned_deptime = datetime.datetime.strptime(vplanned_deptime, "%H:%M").time()
        except Exception, e:
            vplanned_deptime = None

    	#planned_actdeptime
        #duration
        vplanned_actdeptime = row[23][0:2] + ":" + row[23][2:4]
        try:
            vplanned_actdeptime = datetime.datetime.strptime(vplanned_actdeptime, "%H:%M").time()
            vduration = datetime.datetime.utcnow() - datetime.combine(date.today(), vplanned_actdeptime)
            vduration = str(vduration)
        except Exception, e:
            vplanned_actdeptime = None
            vduration = datetime.time(0)


    	#planned_altairport
        vplanned_altairport = row[28]

    	#planned_remarks
        vplanned_remarks = row[29]

        #planned_route
        vplanned_route = row[30]

    	#time_logon
        logon = row[37]
        vtime_logon = logon[0:4] + "-" + logon[4:6] + "-" + logon[6:8] + " " + logon[8:10] + ":" + logon[10:12] + ":" + logon[12:14] + "+0000"

    	#Routestring
        if (row[6] != ''):
            lon = Decimal(row[6])
        else:
            lon = 0.0

        if (row[5] != ''):
            lat = Decimal(row[5])
        else:
            lat = 0.0
        vRoutestring = str(lat) + "," + str(lon) + ";"

    	#total_distance we will deal with when dealing with flights Table

    	#day_night
        vday_night = 0

        #flight_status
        flightstatus = ""

        #altitudeString
        if (row[7] != ''):
            valtitudeString = row[7] + ";"
        else:
            valtitudeString = ""


        ##personal variables

        #pilot_rating
        if (row[16] != ''):
            vpilot_rating = int(row[16])
        else:
            vpilot_rating = -1
        if (vpilot_rating == 0):
            vpilot_rating = 'Not Rated'
        elif (vpilot_rating == 1):
            vpilot_rating = 'VATSIM Online Pilot'
        elif (vpilot_rating == 2):
            vpilot_rating = 'VATSIM Airmanship Basics'
        elif (vpilot_rating == 3):
            vpilot_rating = 'VATSIM VFR Pilot'
        elif (vpilot_rating == 4):
            vpilot_rating = 'VATSIM IFR Pilot'
        elif (vpilot_rating == 5):
            vpilot_rating = 'VATSIM Advanced IFR Pilot'
        elif (vpilot_rating == 6):
            vpilot_rating= 'VATSIM International and Oceanic Pilot'
        elif (vpilot_rating == 7):
            vpilot_rating = 'Helicopter VFR and IFR Pilot'
        elif (vpilot_rating == 8):
            vpilot_rating = 'Military Special Operations Pilot'
        elif (vpilot_rating== 9):
            vpilot_rating = 'VATSIM Pilot Flight Instructor'

        #realname
        vrealname = row[2]

        #ActiveFlights Variables

        #groundspeed
        if (row[8] != ''):
            vgroundspeed = int(row[8])
        else:
            vgroundspeed = 0

        #Personal TABLE - INSERT OR UPDATE
        #########################
        #########################
        if (Personal.objects.filter(cid=vcid).exists() == False):
            newPersonal = Personal(cid = vcid, realname = vrealname, pilot_rating = vpilot_rating)
            newPersonal.save()
        else:
            personal = Personal.objects.get(cid=vcid)
            if (personal.pilot_rating != vpilot_rating):
                personal.pilot_rating = vpilot_rating
                personal.save()


        #Flights TABLE - INSERT OR UPDATE
        #########################
        #########################
        if (Flights.objects.filter(just_date = vjust_date, callsign = vcallsign, cid = vcid).exists() == False):
            #Flight object for this flight doesn't exist yet. Let's create one

            #Let's deal with the rest of the properties of Flights
            #total_distance
            try:
                origAirport = Airports.objects.get(icao=vplanned_depairport)
                origLat = origAirport.lat
                origLon = origAirport.lon
                vtotal_distance = getNmFromLatLon(lat, lon, origLat, origLon)
            except Exception, e:
                vtotal_distance = 0

            #outRamp
            if (vgroundspeed < 50):
                voutRamp = update_time
            else:
                voutRamp = None

        	#offGround
            if (vgroundspeed > 50):
                voffGround = update_time
            else:
                voffGround = None


            #create the new flight
            newFlight = Flights(just_date = vjust_date, callsign = vcallsign, cid = vcid, planned_aircraft = vplanned_aircraft, planned_tascruise = vplanned_tascruise, planned_depairport = vplanned_depairport, planned_altitude = vplanned_altitude, planned_destairport = vplanned_destairport, planned_deptime = vplanned_deptime, planned_actdeptime = vplanned_actdeptime, planned_altairport = vplanned_altairport, planned_remarks = vplanned_remarks, planned_route = vplanned_route, Routestring = vRoutestring, duration = vduration, total_distance = vtotal_distance, time_logon = vtime_logon, offGround = voffGround, outRamp = voutRamp, altitudeString = valtitudeString)
            newFlight.save()

            #these are not dealt with here:
        	#onGround
        	#inGate
        	#groundTime

        else:
            ##Update the flight object
            flight = Flights.objects.get(just_date = vjust_date, callsign = vcallsign, cid = vcid)

            #variables for this section:
            uRouteString = flight.Routestring
            uduration = datetime.datetime.min - datetime.datetime.min
            utotal_distance = flight.total_distance
            uoutRamp = flight.outRamp
            uoffGround = flight.offGround
            uonGround = flight.onGround
            ugroundTime = flight.groundTime

            colonCount = 0
            colon1 = 0
            colon2 = 0
            comma = 0
            rString = flight.Routestring
            try:
                for i in range(len(rString), 0, -1):
                    if ((uRouteString == ";") and (colonCount == 0)):
                        colon1 = i
                        colonCount +=1
                    elif ((uRouteString == ",") and (colonCount == 1)):
                        comma = i
                    elif ((uRouteString == ";") and (colonCount == 1)):
                        colon2 = i
                prevLat = decimal(uRouteString[colon2+1:comma])
                prevLon = decimal(uRouteString[comma+1:colon1])

                #Update Total Distance
                flight.total_distance = flight.total_distance + getNmFromLatLon(lat, lon, prevLat, prevLon)

            except Exception, e:
                flight.total_distance = flight.total_distance + 0

            #Update Route String
            flight.Routestring = flight.Routestring + str(vRoutestring)
            if ((flight.outRamp == None) and (vgroundspeed < 50) and flight.offGround == None):
                flight.outRamp = update_time
                flightStatus = "On The Ground"
            if ((flight.offGround == None) and (vgroundspeed > 50)):
                flight.offGround = update_time
                flightStatus = "Airborne"

            #Get Destination Airport Coords
            try:
                destAirport = Airports.objects.get(icao=vplanned_destairport)
                destLat = destAirport.lat
                destlon = destAirport.lon

                #Update Total Duration
                if ((flight.onGround == None) and (vgroundspeed< 50) and (getNmFromLatLon(lat, lon, destLat, destlon) < 5)):
                    flight.onGround = update_time
                    flightStatus = "Arrived"
                    flight.duration = datetime.datetime.utcnow() #changed

            except Exception as e:
                str(e)

            try:

                if ((flight.offGround != None) and (flight.onGround == None)):
                    tz_info = flight.offGround.tzinfo
                    flight.duration = str(datetime.datetime.now(tz_info) - flight.offGround)
            except Exception as e:
                print str(e)

            if ((flight.offGround != None) and (flight.outRamp != None)):
                #get rid of timezones and converting the strings to datetime format
                outRampshort = str(flight.outRamp)
                offGroundshort = str(flight.offGround)
                outRampshort = datetime.datetime.strptime(outRampshort[:len(outRampshort)-6], "%Y-%m-%d %H:%M:%S")
                offGroundshort = datetime.datetime.strptime(offGroundshort[:len(offGroundshort)-6], "%Y-%m-%d %H:%M:%S")
                gTime = offGroundshort - outRampshort
                gTime = gTime.total_seconds()
                flight.groundTime = gTime

            #update altitude string
            flight.altitudeString = flight.altitudeString + valtitudeString

            flight.save()


        #Deal with ActiveFlights Table
        #########################
        #########################

        #clienttype
        vclienttype = "Pilot"

        #server
        vserver = row[14]

        #altitude
        if (row[7] != ''):
            valtitude = int(row[7])
        else:
            valtitude = 0

        #transponder
        if (row[17] != ''):
            vtransponder = int(row[17])
        else:
            vtransponder = 0

        #heading
        if (row[38] != ''):
            vheading = int(row[38])
        else:
            vheading = 0

        #flight_id
        try:
            associatedFlight = Flights.objects.get(just_date = vjust_date, cid = vcid, callsign = vcallsign)
            vflight_id = associatedFlight.id
        except Exception, e:
            vflight_id = -1

        try:
            aflight = ActiveFlights.objects.get(datetime = update_time, cid = vcid, callsign = vcallsign)
        except Exception, e:
            if (flightstatus == ""):
                try:
                    lastActive = ActiveFlights.objects.filter(cid = vcid, callsign = vcallsign).latest('datetime')
                    flightstatus = lastActive.flight_status
                except Exception, e:
                    flightstatus = " "
            newActive = ActiveFlights(datetime = update_time, cid = vcid, callsign = vcallsign, clienttype = vclienttype, latitude = lat, longitude = lon, server  = vserver, altitude = valtitude, groundspeed = vgroundspeed, transponder = vtransponder, heading = vheading, flight_status=flightstatus, flight_id = vflight_id)
            newActive.save()

        try:
            #ActiveFlights.objects.filter(cid = vcid, callsign = vcallsign).exclude(datetime = update_time)
            oldActive = ActiveFlights.objects.filter(cid = vcid, callsign = vcallsign).exclude(datetime = update_time)
            oldActive.delete()
        except Exception, e:
            pass

    def atcInsert(self, row, update_time):
        #date_time = update_time
        _date = update_time[0:10]

        #realname
        vrealname = row[2]

        #atc_rating
        if (row[16] != ''):
            vatc_rating = int(row[16])
        else:
            vatc_rating = -1

        if (vatc_rating == 1):
            vatc_rating = 'Administrator'
        elif (vatc_rating == 2):
            vatc_rating = 'Supervisor'
        elif (vatc_rating == 3):
            vatc_rating = 'Senior Instructor'
        elif (vatc_rating == 4):
            vatc_rating = 'Instructor'
        elif (vatc_rating == 5):
            vatc_rating = 'Senior Controller'
        elif (vatc_rating == 6):
            vatc_rating = 'Enroute Controller'
        elif (vatc_rating == 7):
            vatc_rating = 'TMA Controller'
        elif (vatc_rating == 8):
            vatc_rating = 'Tower Controller'
        elif (vatc_rating == 9):
            vatc_rating = 'Ground Controller Student'
        elif (vatc_rating == 10):
            vatc_rating = 'Pilot/Observer'
        #datetime
        vdatetime = update_time

        #callsign
    	vcallsign = row[0]

        #cid
    	vcid = row[1]

        #clienttype
    	vclienttype = "ATC"

        #frequency
        if (row[4] != ''):
            vfrequency = row[4]
        else:
            vfrequency = 0.0

        #latitude
    	vlatitude = row[5]

        #longitude
    	vlongitude = row[6]

        #server
    	vserver = row[15]

        #facilitytype
    	vfacilitytype = int(row[18])
        if (vfacilitytype == 0):
            vfacilitytype = 'Other'
        elif (vfacilitytype == 1):
            vfacilitytype = 'Observer'
        elif (vfacilitytype == 2):
            vfacilitytype = 'Clearance Delivery'
        elif (vfacilitytype == 3):
            vfacilitytype = 'Ground'
        elif (vfacilitytype == 4):
            vfacilitytype = 'Tower'
        elif (vfacilitytype == 5):
            vfacilitytype = 'Approach/Departure'
        elif (vfacilitytype == 6):
            vfacilitytype = 'Center'

        #visualrange
        if (row[19] != ''):
            vvisualrange = int(row[19])
        else:
            vvisualrange = 0

        #time_logon
        logon = row[37]
        vtime_logon = logon[0:4] + "-" + logon[4:6] + "-" + logon[6:8] + " " + logon[8:10] + ":" + logon[10:12] + ":" + logon[12:14] + "+0000"
        vtime_logon2 = datetime.datetime.strptime(vtime_logon[:len(vtime_logon)-5], "%Y-%m-%d %H:%M:%S")
        tz_info = vtime_logon2.tzinfo
        vtotaltime = datetime.datetime.now(tz_info) - vtime_logon2
        vtotaltime = str(vtotaltime)
        stripped_update_time = datetime.datetime.strptime(update_time[:len(update_time)-5], "%Y-%m-%d %H:%M:%S")

        if (Personal.objects.filter(cid=vcid).exists() == False):
            newPersonal = Personal(cid = vcid, realname = vrealname, atc_rating = vatc_rating)
            newPersonal.save()
        else:
            personal = Personal.objects.get(cid=vcid)
            if (personal.atc_rating != vatc_rating):
                personal.atc_rating = vatc_rating

        if (ActiveControllers.objects.filter(cid=vcid, callsign=vcallsign, datetime=update_time).exists() == False):
            newActiveATC = ActiveControllers(datetime=update_time, callsign=vcallsign, cid=vcid, clienttype=vclienttype, frequency=vfrequency, latitude=vlatitude, longitude=vlongitude, server=vserver, facilitytype=vfacilitytype, visualrange=vvisualrange, time_logon=vtime_logon)
            newActiveATC.save()
            #delete old active controller
            oldActiveATC = ActiveControllers.objects.filter(cid=vcid, callsign = vcallsign).exclude(datetime = update_time)
            oldActiveATC.delete()


        if (Controllers.objects.filter(date=_date, callsign= vcallsign, cid = vcid).exists() == False):
            newController = Controllers(date =_date, callsign = vcallsign, cid = vcid, facilitytype = vfacilitytype, TotalTime = vtotaltime, lastUpdate = update_time)
            newController.save()
        else:
            controller = Controllers.objects.get(date=_date, callsign= vcallsign, cid=vcid)
            if (stripped_update_time < vtime_logon2):
                controller.TotalTime = controller.TotalTime + vtotaltime
            else:
                str_last_update = str(controller.lastUpdate)
                stripped_last_update = datetime.datetime.strptime(str_last_update[:len(str_last_update)-6], "%Y-%m-%d %H:%M:%S")
                totaltime_delta = (stripped_update_time - stripped_last_update)
                controller.TotalTime  = (datetime.datetime.combine(datetime.date(1,1,1),controller.TotalTime) + totaltime_delta).time()

            controller.lastUpdate = update_time
            controller.save()


    def readVatsim(self):
        client_rows = []
        newUpdate = True
        update = ""
        updateTime = ""

        r = requests.get('http://info.vroute.net/vatsim-data.txt')
        data = r.text.splitlines()

        reader = unicode_csv_reader(data,delimiter=":")

        for row in reader:
            if (row != []):
                if "UPDATE = " in row[0]:
                        update = row[0][9:]
                        updateTime = update[0:4] + "-" + update[4:6] + "-" + update[6:8] + " " + update[8:10] + ":" + update[10:12] + ":" + update[12:14] + "+0000"
                        if (ActiveFlights.objects.filter(datetime=updateTime).exists() == True):
                            newUpdate = False

                elif (row[0] == u'!CLIENTS'):
                    for row in reader:
                        if (row[0] == ";"):
                            break
                        client_rows.append(row)
        if (newUpdate == True):
            for row in client_rows:
                if (row[3] == 'PILOT'):
                    self.pilotInsert(row, updateTime)
                elif (row[3] == 'ATC'):
                    self.atcInsert(row, updateTime)

        ## Delete flights that have been missing for an hour

        notUpdated = ActiveFlights.objects.exclude(datetime = updateTime)
        for flight in notUpdated:
            tz_info = flight.datetime.tzinfo
            if ((flight.datetime + timedelta(hours=1)) <= datetime.datetime.now(tz_info)):
                flight.delete()

        ## Delete missing controllers
        missingController = ActiveControllers.objects.exclude(datetime = updateTime)
        for controller in missingController:
            tz_info = controller.datetime.tzinfo
            if ((controller.datetime + timedelta(hours=1)) <= datetime.datetime.now(tz_info)):
                controller.delete()

    # CSV READING BEGINS
    #
    #
    #

    def handle(self, **options):

        self.readVatsim()
