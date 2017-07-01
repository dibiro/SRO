# -*- encoding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
from Clientes.views import *
from Ordenes.views import *
from Ordenes.models import *
from django.contrib.auth.decorators import login_required


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', login_required(Index.as_view())),
    url(r'^crear_cliente/', crear_cliente),
    url(r'^crear_equipo/', crate_equipos),
    url(r'^login/', login_view),
    url(r'^logout/', logout_view),
    url(r'^get_equipos/', get_equipos),
    url(r'^crear_peticion/', crate_petecion),
    url(r'^lista_clientes/', lista_clientes),
    url(r'^indexAjax/', indexAjax),
    url(r'^update_cliente/', update_cliente),
    url(r'^change_password/', change_password),
    url(r'^update_user/', update_user),
    url(r'^revisar_cedula/', revisar_cedula),
    url(r'^restaurar_super_user/', restaurar_super_user),
    url(r'^lista_telefonos/', lista_telefonos),
    url(r'^lista_pc/', lista_pc),
    url(r'^update_phone/', update_phone),
    url(r'^update_pc/', update_pc),
    url(r'^lista_user/', lista_user),
    url(r'^lista_ordenes/', lista_ordenes),
    url(r'^lista_ordenes_cumplidas/', lista_ordenes_cumplidas),
    url(r'^lista_ordenes_entregadas/', lista_ordenes_entregadas),
    url(r'^lista_bitacora/', lista_bitacora),
    url(r'^delate_ordenes/', delate_ordenes),
    url(r'^completar_orden/', completar_ordenes),
    url(r'^entregar_orden/', entregar_ordenes),
    url(r'^create_user/', create_user),
    url(r'^Factura.pdf/(?P<object_id>\d+)/$', Factura.as_view()),
)

