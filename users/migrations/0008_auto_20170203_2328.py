# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-02-03 23:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_flights_groundtime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flights',
            old_name='planned_destairport',
            new_name='planned_estairport',
        ),
    ]
