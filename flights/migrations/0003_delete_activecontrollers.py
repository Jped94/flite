# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-02-12 16:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0002_auto_20170212_1458'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ActiveControllers',
        ),
    ]
