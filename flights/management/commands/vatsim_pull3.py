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
            vplanned_tascruise = ''

    	#planned_depairport
        vplanned_depairport = row[11]

    	#planned_altitude

        if (row[7] != ''):
            vplanned_altitude = int(row[7])
        else:
            vplanned_altitude = ''

    	#planned_destairport
        vplanned_destairport = row[13]

    	#planned_deptime
        vplanned_deptime = row[22][0:2] + ":" + row[22][2:4]

    	#planned_actdeptime
        #duration
        try:
            vplanned_actdeptime = datetime.datetime.strptime(deptime, "%H:%M")
            vduration = datetime.datetime.utcnow() - datetime.combine(date.today(), fdeptime)
            vduration = str(flight_duration)
        except Exception, e:
            vplanned_actdeptime = ''
            vduration = "00:00"


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
    	#duration
    	#total_distance
    	#day_night
    	#outRamp
    	#offGround
    	#onGround
    	#inGate
    	#groundTime

        self.stdout.write(vjust_date + vcallsign + vcid + vplanned_aircraft + str(vplanned_tascruise) + vplanned_depairport + str(vplanned_altitude) + vplanned_destairport + vplanned_deptime + vplanned_actdeptime + vduration + vplanned_altairport + vplanned_remarks + vplanned_route + vtime_logon, ending='')
        #self.stdout.write(vjust_date + vcallsign + vcid + vplanned_aircraft + str(vplanned_tascruise) + vplanned_depairport + str(vplanned_altitude) + vplanned_destairport + vplanned_deptime + vplanned_actdeptime, ending='')
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
                #elif (row[3] == 'ATC'):
                #    self.atcInsert(row, updateTime)

        ## Delete flights that have been missing for an hour

        #notUpdated = ActiveFlights.objects.exclude(datetime = updateTime)
        #for flight in notUpdated:
            #if ((flight.datetime + timedelta(hours=1)) <= datetime.datetime.utcnow()):
                #flight.delete()
        ## Delete missing controllers
        #missingController = ActiveFlights.objects.exclude(datetime = updateTime)
        #for controller in missingController:
        #    controller.delete()

    # CSV READING BEGINS
    #
    #
    #

    def handle(self, **options):

        self.readVatsim()
