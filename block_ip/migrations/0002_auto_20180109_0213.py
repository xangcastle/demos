# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-01-09 02:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('block_ip', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blockip',
            options={'verbose_name': 'IPs or Mask', 'verbose_name_plural': 'IPs & masks to ban'},
        ),
    ]
