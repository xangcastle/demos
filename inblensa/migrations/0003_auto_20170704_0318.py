# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-07-04 03:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inblensa', '0002_auto_20170304_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='identificacion',
            field=models.CharField(max_length=65, null=True),
        ),
    ]