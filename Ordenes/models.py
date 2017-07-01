from django.db import models
from django.contrib.auth.models import User
from Clientes.models import Clientes, Celulares, Pc


class Ordenes(models.Model):
    TYPE_CHOICES = (("1", "Pc"), ("2", "Celulares"))
    STATUS_CHOICES = (("1", "Recibido"), ("2", "Cumplido"), ("3", "Entregado"), ("4", "Anuladas"))
    object_id = models.BigIntegerField()
    tipo = models.CharField(max_length=2, choices=TYPE_CHOICES, blank=True, null=True)
    estado = models.CharField(max_length=2, choices=STATUS_CHOICES, default='1')
    fecha_de_recibido = models.DateTimeField()
    fecha_de_creacion = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    cliente = models.ForeignKey(Clientes)
    observaciones = models.TextField()
    descripcion = models.TextField()

    class Meta:
        db_table = 'ordenes'

    def get_equipo(self):
        if self.tipo == '1':
            equipo = Pc.objects.get(id=self.object_id)
            return 'Computadora: %s %s' % (equipo.marca, equipo.modelo)
        elif self.tipo == '2':
            equipo = Celulares.objects.get(id=self.object_id)
            return 'Telefono: %s %s' % (equipo.marca, equipo.modelo)

    def get_cliente(self):
        return '(%s) %s %s' % (self.cliente.cedula, self.cliente.nombre, self.cliente.apellido)

    def __unicode__(self):
        return '%s (%s) %s - Estado: %s' % (self.tipo, self.fecha_de_recibido, self.descripcion, self.estado)


class OrdenesCompletar(models.Model):
    orden = models.ForeignKey(Ordenes)
    diagnostico = models.TextField()
    fecha_de_culminacion = models.DateTimeField()
    fecha_de_creacion = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    observaciones = models.TextField()
    garantia = models.PositiveIntegerField()

    class Meta:
        db_table = 'ordenes_completadas'

    def __unicode__(self):
        return '%s (%s) %s' % (self.orden, self.fecha_de_culminacion, self.diagnostico)


class OrdenesEntragadas(models.Model):
    orden = models.ForeignKey(OrdenesCompletar)
    fecha_de_entrega = models.DateTimeField()
    fecha_de_creacion = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    cliente = models.ForeignKey(Clientes)

    class Meta:
        db_table = 'entrega_ordenes'

    def __unicode__(self):
        return '%s (%s) %s' % (self.orden, self.fecha_de_entrega, self.cliente)