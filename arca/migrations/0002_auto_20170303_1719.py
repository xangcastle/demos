# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-03-03 23:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('arca', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comercio_categoria',
            options={'verbose_name': 'Categoria', 'verbose_name_plural': 'Categorias de comercio'},
        ),
    ]