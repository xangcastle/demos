# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import arca.models
from django.db import migrations, models
import django.db.models.deletion
import geoposition.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Codigo_Descuento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(blank=True, default=uuid.uuid4, max_length=100, unique=True)),
                ('canjeado', models.BooleanField(default=False)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('actualizado', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comercio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
                ('nombre', models.CharField(blank=True, max_length=100, null=True)),
                ('direccion', models.CharField(blank=True, max_length=500, null=True)),
                ('position', geoposition.fields.GeopositionField(blank=True, max_length=42, null=True)),
                ('telefono', models.CharField(blank=True, max_length=10, null=True)),
                ('identificacion', models.CharField(blank=True, max_length=50, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to=arca.models.get_media_url)),
                ('tiene_descuento_vigencia', models.BooleanField(default=False)),
                ('tiene_descuento_compra_minima', models.BooleanField(default=False)),
                ('tiene_servicio_afiliacion', models.BooleanField(default=False)),
                ('tiene_servicio_crm', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comercio_Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias de comercio',
            },
        ),
        migrations.CreateModel(
            name='Descuento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=100, null=True)),
                ('porcentaje_descuento', models.FloatField()),
                ('vigencia', models.IntegerField()),
                ('desc_dia_vigencia', models.IntegerField(blank=True, null=True)),
                ('desc_dia_vigencia_porc_inf', models.FloatField(blank=True, null=True)),
                ('desc_dia_vigencia_porc_sup', models.FloatField(blank=True, null=True)),
                ('desc_compra_minima', models.FloatField(blank=True, null=True)),
                ('desc_compra_minima_porc_inf', models.FloatField(blank=True, null=True)),
                ('desc_compra_minima_porc_sup', models.FloatField(blank=True, null=True)),
                ('tipo_cambio', models.FloatField(default=1)),
                ('activo', models.BooleanField(default=True)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('actualizado', models.DateTimeField(auto_now=True)),
                ('comercio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arca.Comercio')),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
                ('nombre', models.CharField(blank=True, max_length=100, null=True)),
                ('apellido', models.CharField(blank=True, max_length=100, null=True)),
                ('direccion', models.CharField(blank=True, max_length=500, null=True)),
                ('telefono', models.CharField(blank=True, max_length=10, null=True)),
                ('fecha_alta', models.DateTimeField(auto_now_add=True)),
                ('fecha_baja', models.DateTimeField(blank=True, null=True)),
                ('comercio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arca.Comercio')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('documento', models.TextField(blank=True, null=True)),
                ('monto', models.FloatField(blank=True, null=True)),
                ('descuento', models.FloatField(blank=True, null=True)),
                ('fecha', models.DateTimeField(auto_now=True)),
                ('comercio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='arca.Comercio')),
                ('cupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='arca.Codigo_Descuento')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=500)),
                ('precio', models.FloatField()),
                ('descuento', models.FloatField(blank=True, null=True)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to=arca.models.get_media_url)),
                ('activo', models.BooleanField(default=True)),
                ('comercio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='arca.Comercio')),
            ],
        ),
        migrations.CreateModel(
            name='Publicidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('banner', models.ImageField(blank=True, null=True, upload_to=arca.models.get_media_url)),
                ('activo', models.BooleanField(default=True)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('actualizado', models.DateTimeField(auto_now=True)),
                ('baja', models.DateTimeField(blank=True, null=True)),
                ('commercio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arca.Comercio')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
                ('nombre', models.CharField(blank=True, max_length=100, null=True)),
                ('apellido', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('foto', models.ImageField(null=True, upload_to=arca.models.get_media_url)),
                ('telefono', models.CharField(blank=True, max_length=20, null=True)),
                ('direccion', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='comercio',
            name='categoria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rel_comercio_categoria', to='arca.Comercio_Categoria'),
        ),
        migrations.AddField(
            model_name='codigo_descuento',
            name='actualizado_por',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Descuento_Empleado_Update', to='arca.Empleado'),
        ),
        migrations.AddField(
            model_name='codigo_descuento',
            name='cliente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='arca.Usuario'),
        ),
        migrations.AddField(
            model_name='codigo_descuento',
            name='creado_por',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Descuento_Empleado_Create', to='arca.Empleado'),
        ),
        migrations.AddField(
            model_name='codigo_descuento',
            name='descuento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arca.Descuento'),
        ),
    ]
