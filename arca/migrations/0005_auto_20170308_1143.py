# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-03-08 17:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arca', '0004_auto_20170308_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comercio',
            name='direccion',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='comercio',
            name='telefono',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]