from django.contrib.admin.models import LogEntry
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from .models import *


admin.site.register(LogEntry)
admin.site.register(Clientes)
admin.site.register(Direccion)
admin.site.register(Telefono)
admin.site.register(Celulares)
admin.site.register(Pc)
admin.site.register(Bitacora)