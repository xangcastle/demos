from __future__ import unicode_literals
from django.db.models import Sum
from django.db import models
from django.forms import model_to_dict


class Base(models.Model):
    def to_json(self):
        return model_to_dict(self)

    class Meta:
        abstract = True


class Empleado(Base):
    nombre = models.CharField(max_length=255)
    cedula = models.CharField(max_length=14)
    inss = models.CharField(max_length=14, verbose_name="numero de inss", null=True, blank=True)
    salario = models.FloatField(verbose_name="salario mensual", default=5000.00)
    transporte = models.FloatField(default=1200, verbose_name="viaticos de transporte")
    alimentacion = models.FloatField(default=1200, verbose_name="viaticos de alimentacion")
    fecha_ingreso = models.DateField(verbose_name="fecha de ingreso")
    cargo = models.CharField(max_length=255)
    cargo_descripcion = models.TextField(max_length=400, verbose_name="breve descripcion del cargo")
    foto = models.ImageField(null=True, blank=True)
    contrato = models.FileField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __unicode__(self):
        return self.nombre

    def salario_quincenal(self):
        return round(self.salario / 2, 2)


class Planilla(Base):
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def pagos(self):
        return PagoEmpleado.objects.filter(planilla=self)

    def empleados(self):
        return Empleado.objects.filter(id__in=self.pagos().values_list('empleado', flat=True))

    def cargar(self):
        empleados = Empleado.objects.all().exclude(id__in=self.empleados())
        data = []
        for e in empleados:
            p, created = PagoEmpleado.objects.get_or_create(planilla=self, empleado=e, salario=e.salario/2,
                                                            alimentacion=e.alimentacion/2, transporte=e.transporte/2)
            data.append(p)
        return data

    def save(self, *args, **kwargs):
        super(Planilla, self).save()
        self.cargar()


    def total_salarios(self):
        return round(self.pagos().aggregate(Sum('salario'))['salario__sum'], 2)

    def total_inss_laboral(self):
        return round(self.pagos().aggregate(Sum('inss_laboral'))['inss_laboral__sum'], 2)

    def total_prestamos(self):
        return round(self.pagos().aggregate(Sum('prestamo'))['prestamo__sum'], 2)

    def total_transporte(self):
        return round(self.pagos().aggregate(Sum('transporte'))['transporte__sum'], 2)

    def total_alimentacion(self):
        return round(self.pagos().aggregate(Sum('alimentacion'))['alimentacion__sum'], 2)

    def total_pagos(self):
        return round(self.total_salarios() - (self.total_inss_laboral() + self.total_prestamos()), 2)

    def total_viaticos(self):
        return round((self.total_alimentacion() + self.total_transporte()), 2)

class PagoEmpleado(Base):
    planilla = models.ForeignKey(Planilla)
    empleado = models.ForeignKey(Empleado)
    salario = models.FloatField(default=0.0)
    inss_patronal = models.FloatField(default=0.0)
    inss_laboral = models.FloatField(default=0.0)
    prestamo = models.FloatField(default=0.0)
    inatec = models.FloatField(default=0.0)
    alimentacion = models.FloatField(default=0.0)
    transporte = models.FloatField(default=0.0)

    def total_deduccion(self):
        return round(self.inss_laboral + self.prestamo, 2)

    def viaticos(self):
        return round(self.transporte + self.alimentacion, 2)

    def neto_recibir(self):
        return round(self.salario - self.total_deduccion(), 2)

    def save(self, *args, **kwargs):
        self.inss_laboral = round(self.salario * 0.0625, 2)
        self.inss_patronal = round(self.salario * 0.19, 2)
        self.inatec = round(self.salario * 0.02, 2)
        super(PagoEmpleado, self).save(*args, **kwargs)
