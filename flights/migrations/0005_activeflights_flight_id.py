# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-02-12 23:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0004_flights_altitudestring'),
    ]

    operations = [
        migrations.AddField(
            model_name='activeflights',
            name='flight_id',
            field=models.IntegerField(default=20),
            preserve_default=False,
        ),
    ]
