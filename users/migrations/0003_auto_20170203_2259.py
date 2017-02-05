# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-02-03 22:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20170203_2259'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveControllers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('callsign', models.CharField(max_length=10)),
                ('cid', models.CharField(max_length=30)),
                ('clienttype', models.CharField(max_length=10)),
                ('frequency', models.DecimalField(decimal_places=3, max_digits=6)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=8)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('server', models.CharField(max_length=15)),
                ('facilitytype', models.CharField(max_length=30)),
                ('visualrange', models.IntegerField()),
                ('time_logon', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Aircrafts',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('aircraft_type', models.CharField(max_length=1)),
                ('mfgr', models.CharField(max_length=30)),
                ('model', models.CharField(max_length=30)),
                ('code', models.CharField(max_length=4)),
                ('engineqty', models.IntegerField()),
                ('enginetype', models.CharField(max_length=1)),
                ('weightclass', models.CharField(max_length=1)),
                ('descentrate', models.CharField(max_length=10)),
                ('serviceceiling', models.CharField(max_length=10)),
                ('cruisetas', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Airlines',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('icao', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('radio', models.CharField(max_length=100, null=True)),
                ('website', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Airports',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('icao', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('lat', models.DecimalField(decimal_places=6, max_digits=9)),
                ('lon', models.DecimalField(decimal_places=6, max_digits=10)),
                ('alt', models.IntegerField(null=True)),
                ('iata', models.CharField(max_length=4, null=True)),
                ('city', models.CharField(max_length=50, null=True)),
                ('iso', models.CharField(max_length=2)),
                ('FIR', models.CharField(max_length=4, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Controllers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('callsign', models.CharField(max_length=10)),
                ('cid', models.CharField(max_length=30)),
                ('facilitytype', models.CharField(max_length=1)),
                ('TotalTime', models.TimeField()),
                ('lastUpdate', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Isocodes',
            fields=[
                ('code', models.CharField(max_length=2, primary_key=True, serialize=False)),
                ('country', models.CharField(max_length=100)),
                ('cleaned', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Registrations',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('prefix', models.CharField(max_length=5)),
                ('iso', models.CharField(max_length=2, null=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='activecontrollers',
            unique_together=set([('datetime', 'callsign', 'cid')]),
        ),
    ]
