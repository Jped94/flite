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

class Command(NoArgsCommand):

    def handle(self, *args, **options):
        user = Personal.objects.get(cid = "123456")
        self.stdout.write(user.cid)
