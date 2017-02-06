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
                        date = row[0]
                        update = date[9:]
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
