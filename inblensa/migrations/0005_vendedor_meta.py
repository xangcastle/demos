# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-09-04 17:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inblensa', '0004_auto_20170829_1950'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendedor',
            name='meta',
            field=models.FloatField(default=0.0),
        ),
    ]
