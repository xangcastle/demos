# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-09-04 17:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inblensa', '0005_vendedor_meta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendedor',
            name='meta',
            field=models.FloatField(default=1.0),
        ),
    ]
