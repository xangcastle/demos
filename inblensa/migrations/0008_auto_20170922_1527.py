# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-09-22 15:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inblensa', '0007_auto_20170922_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='comentarios',
            field=models.ManyToManyField(blank=True, to='inblensa.Comentario'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='gestiones',
            field=models.ManyToManyField(blank=True, to='inblensa.Gestion'),
        ),
        migrations.AlterField(
            model_name='import',
            name='identificacion',
            field=models.CharField(blank=True, max_length=65, null=True),
        ),
    ]