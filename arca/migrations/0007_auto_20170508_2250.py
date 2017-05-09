# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-05-08 22:50
from __future__ import unicode_literals

import arca.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arca', '0006_usuario_codigo'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='age',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='usuario',
            name='gender',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='comercio',
            name='direccion',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to=arca.models.get_media_url),
        ),
    ]
