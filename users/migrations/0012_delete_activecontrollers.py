# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-02-12 14:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20170205_1639'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ActiveControllers',
        ),
    ]
