from django.contrib.admin.models import LogEntry
from django.contrib import admin
from .models import *

admin.site.register(Ordenes)
admin.site.register(OrdenesCompletar)
admin.site.register(OrdenesEntragadas)