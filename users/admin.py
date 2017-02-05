from django.contrib import admin

from .models import Flights, Personal

admin.site.register(Personal)
admin.site.register(Flights)

# Register your models here.
