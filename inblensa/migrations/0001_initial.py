# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-21 16:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import inblensa.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bodega',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('encargado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bodega_Detalle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('existencia', models.FloatField(default=0.0)),
                ('bodega', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inblensa.Bodega')),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identificacion', models.CharField(max_length=65)),
                ('nombre', models.CharField(max_length=165)),
                ('telefono', models.CharField(blank=True, max_length=50, null=True)),
                ('celular', models.CharField(blank=True, max_length=50, null=True)),
                ('contacto', models.CharField(blank=True, max_length=150, null=True)),
                ('direccion', models.TextField(blank=True, max_length=600, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=400)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Documento_Abono',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto_abono', models.FloatField()),
                ('fecha_abono', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Documento_Cobro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nodoc', models.CharField(max_length=15, null=True, verbose_name='numero de documento')),
                ('descripcion', models.CharField(blank=True, max_length=300, null=True)),
                ('monto', models.FloatField()),
                ('impuesto', models.FloatField()),
                ('total', models.FloatField()),
                ('fecha', models.DateField()),
                ('fecha_vence', models.DateField(blank=True, null=True)),
                ('pagada', models.BooleanField(default=False)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inblensa.Cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razon_social', models.CharField(max_length=255)),
                ('numero_ruc', models.CharField(max_length=14)),
            ],
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_fac', models.CharField(max_length=10)),
                ('serie', models.CharField(default='A', max_length=2)),
                ('stotal', models.FloatField()),
                ('impuesto', models.FloatField()),
                ('total', models.FloatField()),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('anulada', models.BooleanField(default=False)),
                ('fecha_anulacion', models.DateTimeField(null=True)),
                ('comentario', models.CharField(max_length=200, null=True)),
                ('fecha_vence', models.DateTimeField(blank=True, null=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventario_factura_cliente', to='inblensa.Cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Factura_Abono',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto_abono', models.FloatField()),
                ('fecha_abono', models.DateField(auto_now_add=True)),
                ('factura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inblensa.Factura')),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Factura_Detalle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.FloatField()),
                ('valor', models.FloatField()),
                ('entregado', models.BooleanField(default=False)),
                ('bodega', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inblensa.Bodega')),
                ('factura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inblensa.Factura')),
            ],
        ),
        migrations.CreateModel(
            name='Forma_Pago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forma_pago', models.CharField(max_length=50)),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Forma de pago',
                'verbose_name_plural': 'formas de pago',
            },
        ),
        migrations.CreateModel(
            name='Gestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_completa', models.DateTimeField(null=True)),
                ('descripcion', models.TextField(max_length=400, null=True)),
                ('descripcion_resultado', models.CharField(max_length=400, null=True)),
                ('programacion', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Gestion_Resultado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Import',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razon_social', models.CharField(max_length=255)),
                ('numero_ruc', models.CharField(max_length=20)),
                ('nombre', models.CharField(max_length=165)),
                ('identificacion', models.CharField(max_length=65)),
                ('telefono', models.CharField(max_length=50)),
                ('celular', models.CharField(blank=True, max_length=50, null=True)),
                ('direccion', models.TextField(max_length=600)),
                ('contacto', models.CharField(max_length=150)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('nodoc', models.CharField(blank=True, max_length=15, null=True, verbose_name='numero de documento')),
                ('descripcion', models.CharField(blank=True, max_length=500, null=True)),
                ('monto', models.FloatField(blank=True, null=True)),
                ('impuesto', models.FloatField(blank=True, null=True)),
                ('total', models.FloatField(blank=True, null=True)),
                ('abono', models.FloatField(blank=True, null=True)),
                ('fecha', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'opcion',
                'verbose_name_plural': 'importacion de datos',
            },
        ),
        migrations.CreateModel(
            name='Import_Imventario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razon_social', models.CharField(max_length=255)),
                ('numero_ruc', models.CharField(max_length=14)),
                ('producto_codigo', models.CharField(max_length=50)),
                ('producto_serie', models.CharField(max_length=50)),
                ('producto_nombre', models.CharField(max_length=200)),
                ('producto_existencia', models.FloatField(default=0)),
                ('producto_costo', models.FloatField(default=0)),
                ('producto_precio', models.FloatField(default=0)),
                ('producto_marca', models.CharField(max_length=100)),
                ('producto_categoria', models.CharField(max_length=100)),
                ('producto_medida', models.CharField(max_length=100)),
                ('bodega', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'opcion',
                'verbose_name_plural': 'importacion de productos',
            },
        ),
        migrations.CreateModel(
            name='Moneda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('simbolo', models.CharField(max_length=4)),
                ('activo', models.BooleanField(default=True)),
                ('principal', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_pedido', models.IntegerField(blank=True, null=True)),
                ('stotal', models.FloatField(verbose_name='subtotal')),
                ('impuesto', models.FloatField()),
                ('total', models.FloatField()),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('anulado', models.BooleanField(default=False)),
                ('fecha_anulacion', models.DateTimeField(null=True)),
                ('comentario', models.CharField(max_length=200, null=True)),
                ('cerrado', models.BooleanField(default=False)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inblensa.Cliente')),
                ('usuario_anulacion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pedido_usuario_anulacion', to=settings.AUTH_USER_MODEL)),
                ('usuario_creacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedido_usuario_creacion', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pedido_Detalle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.FloatField()),
                ('valor', models.FloatField()),
                ('bodega', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inblensa.Bodega')),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inblensa.Pedido')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=50)),
                ('serie', models.CharField(blank=True, max_length=50, null=True)),
                ('nombre', models.CharField(max_length=200)),
                ('costo_promedio', models.FloatField(default=0)),
                ('precio', models.FloatField(default=0)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to=inblensa.models.get_media_url)),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'producto',
                'verbose_name_plural': 'Productos del Inventario',
            },
        ),
        migrations.CreateModel(
            name='Producto_Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoria', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Producto_Marca',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marca', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Producto_Medida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medida', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto', models.ImageField(null=True, upload_to=inblensa.models.get_media_url)),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inblensa.Empresa')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Recibo_Provicional',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_recibo', models.IntegerField()),
                ('monto', models.FloatField()),
                ('cancelacion', models.BooleanField()),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('comentario', models.CharField(max_length=600, null=True)),
                ('fecha_cobro_ck', models.DateTimeField(blank=True, null=True)),
                ('referencia', models.CharField(blank=True, max_length=20, null=True)),
                ('cerrado', models.BooleanField(default=False)),
                ('anulado', models.BooleanField(default=False)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inblensa.Cliente')),
                ('forma_pago', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inblensa.Forma_Pago')),
                ('usuario_creacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Recibo_Provicional_User_Creacion', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Recibo Provicional',
                'verbose_name_plural': 'Recibos Provicionales de Caja',
            },
        ),
        migrations.CreateModel(
            name='Tipo_Cambio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cambio', models.FloatField()),
                ('fecha', models.DateField()),
                ('moneda', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inblensa.Moneda')),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_Gestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('activo', models.BooleanField(default=True)),
                ('resultados', models.ManyToManyField(blank=True, to='inblensa.Gestion_Resultado')),
            ],
        ),
        migrations.CreateModel(
            name='Vendedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serie', models.CharField(blank=True, max_length=25, null=True, verbose_name='Serie de Recibos')),
                ('numero_inicial', models.PositiveIntegerField(blank=True, null=True, verbose_name='Numero Inicial para los recibos')),
                ('activo', models.BooleanField(default=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'vendedores',
            },
        ),
        migrations.AddField(
            model_name='producto',
            name='categoria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inblensa.Producto_Categoria'),
        ),
        migrations.AddField(
            model_name='producto',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inblensa.Empresa'),
        ),
        migrations.AddField(
            model_name='producto',
            name='marca',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inblensa.Producto_Marca'),
        ),
        migrations.AddField(
            model_name='producto',
            name='medida',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inblensa.Producto_Medida'),
        ),
        migrations.AddField(
            model_name='pedido_detalle',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inblensa.Producto'),
        ),
        migrations.AddField(
            model_name='pedido',
            name='vendedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedido_usuario_vendedor', to='inblensa.Vendedor'),
        ),
        migrations.AddField(
            model_name='gestion',
            name='resultado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inblensa.Gestion_Resultado'),
        ),
        migrations.AddField(
            model_name='gestion',
            name='tipo_gestion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inblensa.Tipo_Gestion'),
        ),
        migrations.AddField(
            model_name='gestion',
            name='usuario_completa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usuario_completa', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='gestion',
            name='usuario_creacion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usuario_creacion', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='factura_detalle',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inblensa.Producto'),
        ),
        migrations.AddField(
            model_name='factura',
            name='moneda',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inblensa.Moneda'),
        ),
        migrations.AddField(
            model_name='factura',
            name='usuario_anulacion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='factura_usuario_anulacion', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='factura',
            name='usuario_creacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='factura_usuario_creacion', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='documento_cobro',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inblensa.Empresa'),
        ),
        migrations.AddField(
            model_name='documento_abono',
            name='documento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inblensa.Documento_Cobro'),
        ),
        migrations.AddField(
            model_name='documento_abono',
            name='usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cliente',
            name='comentarios',
            field=models.ManyToManyField(to='inblensa.Comentario'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inblensa.Empresa'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='gestiones',
            field=models.ManyToManyField(to='inblensa.Gestion'),
        ),
        migrations.AddField(
            model_name='bodega_detalle',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inblensa.Producto'),
        ),
    ]
