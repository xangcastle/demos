# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-03-10 17:59
from __future__ import unicode_literals

import arca.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('arca', '0009_auto_20170309_0517'),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto', models.ImageField(null=True, upload_to=arca.models.get_media_url)),
                ('telefono', models.CharField(blank=True, max_length=20, null=True)),
                ('direccion', models.CharField(blank=True, max_length=500, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Arca_Profile_Usuario', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
