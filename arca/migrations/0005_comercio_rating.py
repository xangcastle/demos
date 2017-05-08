# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-04-30 22:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('arca', '0004_descuento_es_gratuito'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comercio_Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=1)),
                ('comercio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arca.Comercio')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arca.Usuario')),
            ],
        ),
    ]