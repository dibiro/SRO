# -*- encoding: utf-8 -*-
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render_to_response, HttpResponse, render
from django.template import RequestContext
from .models import * 
from Clientes.models import * 
import json
from django.conf import settings as _settings
from django.contrib.auth import login, logout, authenticate
from django.utils.module_loading import import_by_path
from django.core.mail import get_connection, send_mail, BadHeaderError
from easy_pdf.views import PDFTemplateView
import datetime


def crate_petecion(request):
    orden = Ordenes(
        cliente_id=request.POST['cliente'],
        object_id=request.POST['object_id'],
        tipo=request.POST['tipo'],
        fecha_de_recibido=request.POST['fecha_de_recibido'],
        user=request.user,
        observaciones=request.POST['observaciones'],
        descripcion=request.POST['descripcion'],
    )
    orden.save()
    bitacora = Bitacora(
        tipo='4',
        object_id=orden.id,
        accion='1',
        user=request.user,
        descripcion='Se registra la peticion numero: ' + str(orden.id) + ', a nombre de: ' + orden.get_cliente() + ', ' + orden.get_equipo() + ' fecha_de_recibido: ' + request.POST['fecha_de_recibido'] + ', ' + 'observaciones: ' + request.POST['observaciones'] + ', ' + 'descripcion: ' + request.POST['descripcion'] + ', ',
    )
    bitacora.save()
    result = json.dumps(orden.id, ensure_ascii=False)
    return HttpResponse(result, content_type='application/json; charset=utf-8')


def lista_ordenes(request):
    ordenes = Ordenes.objects.all()
    pcs = Pc.objects.all()
    cell = Celulares.objects.all()
    return render(request, 'lista_ordenes.html', {'ordenes': ordenes, 'pcs' : pcs , 'cell' : cell})


def delate_ordenes(request):
    orden = Ordenes.objects.get(id=request.POST['id'])
    if orden.estado == '1':
        orden.estado = '4'
        orden.save()
        bitacora = Bitacora(
            tipo='4',
            object_id=orden.id,
            accion='3',
            user=request.user,
            descripcion='Se elimina la peticion numero: ' + str(orden.id),
        )
        bitacora.save()
    result = json.dumps('Eliminado', ensure_ascii=False)
    return HttpResponse(result, content_type='application/json; charset=utf-8')


def lista_ordenes_cumplidas(request):
    ordenes = OrdenesCompletar.objects.all().order_by('fecha_de_recibido')
    dicc = {}
    lista = []
    for x in ordenes:
        dicc = {
            'id': x.id,
            'tipo' : x.tipo,
            'estado' : x.estado,
            'fecha_de_recibido' : x.fecha_de_recibido.strftime('%Y-%m-%d'),
            'fecha_de_creacion' : x.fecha_de_creacion,
            'user' : x.user,
            'cliente' : '(' + x.cliente.cedula + ') '+ x.cliente.nombre + ' ' + x.cliente.apellido,
            'observaciones' : x.observaciones,
            'descripcion' : x.descripcion,
        }
        if x.tipo == 1:
            e = Pc.objects.get(id=x.object_id)
            dicc['equipo'] = e.marca + ' ' + e.modelo
        else:
            e = Celulares.objects.get(id=x.object_id)
            dicc['equipo'] = e.marca + ' ' + e.modelo
        lista.append(dicc)
        dicc = {}
    return render(request, 'lista_ordenes.html', {'ordenes': lista,})


def completar_ordenes(request):
    orden = Ordenes.objects.get(id=request.POST['id'])
    if orden.estado == '1':
        ordenc = OrdenesCompletar(
            orden_id=request.POST['id'],
            diagnostico=request.POST['diagnostico'],
            fecha_de_culminacion=request.POST['fecha_de_culminacion'],
            user=request.user,
            observaciones=request.POST['observaciones'],
            garantia=request.POST['garantia'],
        )
        ordenc.save()
        orden.estado = '2'
        orden.save()
        bitacora = Bitacora(
            tipo='5',
            object_id=ordenc.id,
            accion='1',
            user=request.user,
            descripcion='Se cambia a completado la peticion numero: ' + str(orden.id) + ', diagnostico: ' + request.POST['diagnostico'] + ', ' + 'fecha de culminacion: ' + request.POST['fecha_de_culminacion'] + ', ' + 'observaciones: ' + request.POST['observaciones'] + ', ' + 'garantia: ' + request.POST['garantia'],
        )
        bitacora.save()
    result = json.dumps('1', ensure_ascii=False)
    return HttpResponse(result, content_type='application/json; charset=utf-8')


def entregar_ordenes(request):
    ordenc = OrdenesCompletar.objects.get(id=request.POST['id'])
    orden = Ordenes.objects.get(id=ordenc.orden.id)
    if ordenc.orden.estado == '2':
        orden_E = OrdenesEntragadas(
            user=request.user,
            orden_id=request.POST['id'],
            cliente_id=request.POST['cliente'],
            fecha_de_entrega=request.POST['fecha_entrega'],
        )
        orden_E.save()
        orden.estado = '3'
        orden.save()
        bitacora = Bitacora(
            tipo='6',
            object_id=orden_E.id,
            accion='1',
            user=request.user,
            descripcion='Se cambia a entregada la peticion numero: ' + str(orden.id) + ', recivido por: ' + orden.get_cliente() + ', ' + 'fecha de entrega: ' + request.POST['fecha_entrega'],
        )
        bitacora.save()
    result = json.dumps('1', ensure_ascii=False)
    return HttpResponse(result, content_type='application/json; charset=utf-8')


def lista_ordenes_cumplidas(request):
    ordenes = OrdenesCompletar.objects.all().order_by('fecha_de_culminacion')
    clientes = Clientes.objects.all()
    pcs = Pc.objects.all()
    cell = Celulares.objects.all()
    return render(request, 'lista_ordenes_cumplidas.html', {'ordenes': ordenes , 'pcs' : pcs , 'cell' : cell , 'clientes' : clientes})


def lista_ordenes_entregadas(request):
    ordenes = OrdenesEntragadas.objects.all().order_by('fecha_de_entrega')
    pcs = Pc.objects.all()
    cell = Celulares.objects.all()
    return render(request, 'lista_ordenes_entregadas.html', {'ordenes': ordenes , 'pcs' : pcs , 'cell' : cell})


class Factura(PDFTemplateView):
    template_name = "factura.html"

    def get_context_data(self, object_id, **kwargs):
        fecha=datetime.date.today()
        requests=Ordenes.objects.get(id=object_id)
        if requests.tipo == "1":
            equipo = Pc.objects.get(id=requests.object_id)
        else:
            equipo = Celulares.objects.get(id=requests.object_id)
        return super(Factura, self).get_context_data(
            pagesize="A4 landscape",
            title="Peticiones",
            requests=requests,
            equipo=equipo,
            fecha=fecha,
            **kwargs
        )