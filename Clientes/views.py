# -*- encoding: utf-8 -*-
from django.views.generic import TemplateView
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render_to_response, HttpResponse, render
from django.template import RequestContext
from .models import * 
import json
from django.conf import settings as _settings
from django.contrib.auth import login, logout, authenticate
from django.utils.module_loading import import_by_path
from django.core.mail import get_connection, send_mail, BadHeaderError


def login_view(request):
    logout(request)
    username = password = ''
    next = ""
    redirect_to = getattr(_settings, 'LOGIN_REDIRECT_URL', None)
    if request.GET:
        next = request.GET['next']
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        auth_backend = import_by_path('django.contrib.auth.backends.ModelBackend')()
        user = auth_backend.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                user.backend = "%s.%s" % (import_by_path('django.contrib.auth.backends.ModelBackend')().__module__, import_by_path('django.contrib.auth.backends.ModelBackend')().__class__.__name__)
                login(request, user)
                if next == "":
                    return HttpResponseRedirect('/')
                else:
                    return HttpResponseRedirect(next)
        else:
            return HttpResponseRedirect('/')
    return render_to_response(
        'login.html',
        {
            'username': username,
            'next': next,
        },
        context_instance=RequestContext(request)
    )


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


class Index(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        clientes = Clientes.objects.all()
        return render_to_response(self.template_name, locals(), context_instance=RequestContext(request))


def crear_cliente(request):
    cliente = Clientes(
        cedula=request.POST['cedula'],
        nombre=request.POST['nombre'],
        sexo=request.POST['sexo'],
        apellido=request.POST['apellido'],
        fecha_de_nacimiento=request.POST['fecha_de_nacimiento'],
    )
    cliente.save()
    bitacora = Bitacora(
        tipo='1',
        object_id=cliente.id,
        accion='1',
        user=request.user,
    )
    descripcion='Se Registra al cliente Cedula: ' + cliente.cedula + ', ' + cliente.nombre + ' ' + cliente.apellido + ', sexo: ' + cliente.get_sex() + ', Fecha de nacimiento: ' + cliente.fecha_de_nacimiento
    telefonos = request.POST.getlist('telefonos[]')
    direcciones = request.POST.getlist('direcciones[]')
    aux = 1 
    for x in telefonos:
        if x != '':
            telefono = Telefono(
                cliente=cliente,
                telefono=x,
            )
            telefono.save()
            if aux == 1:
                descripcion += ' telefono(s): ' + x + ', '
            else:
                descripcion += x + ', ' 
            aux += 1
    aux = 1 
    for x in direcciones:
        if x != '':
            direccion = Direccion(
                cliente=cliente,
                direccion=x,
            )
            direccion.save()
            if aux == 1:
                descripcion += ' direccion(es): ' + x + ', '
            else:
                descripcion += x + ', '
            aux += 1
    bitacora.descripcion = descripcion
    bitacora.save()
    clientes = Clientes.objects.all()
    lista = []
    dicc = {}
    for x in clientes:
        dicc = {
            'id': x.id,
            'nombre': x.cedula + ' - ' + x.nombre + ' ' + x.apellido,
        }
        lista.append(dicc)
        dicc = {}
    dicc = {
        'clientes': lista,
        'nuevo': cliente.id,
    }
    result = json.dumps(dicc, ensure_ascii=False)
    return HttpResponse(result, content_type='application/json; charset=utf-8')


def get_equipos(request):
    if request.POST['tipo'] == '1':
        equipos = Pc.objects.filter(cliente=request.POST['cliente'])
    elif request.POST['tipo'] == '2':
        equipos = Celulares.objects.filter(cliente=request.POST['cliente'])
    lista = []
    for x in equipos:
        dicc = {}
        dicc = {
            'id': x.id,
            'name': x.marca + ' - ' + x.modelo,
        }
        lista.append(dicc)
    result = json.dumps(lista, ensure_ascii=False)
    return HttpResponse(result, content_type='application/json; charset=utf-8')


def crate_equipos(request):
    tipo = 2
    descripcion = ''
    if request.POST['tipo'] == '1':
        equipo = Pc(
            cliente_id=request.POST['cliente'],
            marca=request.POST['marca'],
            modelo=request.POST['modelo'],
            HDD=request.POST['HDD'],
            tarjeta_madre=request.POST['tarjeta_madre'],
            CPU=request.POST['CPU'],
            RAM=request.POST['RAM'],
            unida_DVD=request.POST['unida_DVD'],
            fuente_de_poder=request.POST['fuente_de_poder'],
            observaciones=request.POST['observaciones'],
        )
        equipo.save()
        descripcion = 'Se registra telefono a nombre de: ' + equipo.cliente.cedula + 'marca:' + request.POST['marca'] + 'modelo:' + request.POST['modelo'] + 'HDD:' + request.POST['HDD'] + 'tarjeta_madre:' + request.POST['tarjeta_madre'] + 'CPU:' + request.POST['CPU'] + 'RAM:' + request.POST['RAM'] + 'unida DVD:' + request.POST['unida_DVD'] + 'fuente de poder:' + request.POST['fuente_de_poder'] + 'observaciones:' + request.POST['observaciones']
    elif request.POST['tipo'] == '2':
        tipo = 3
        equipo = Celulares(
            cliente_id=request.POST['cliente'],
            marca=request.POST['marca'],
            modelo=request.POST['modelo'],
            serial=request.POST['serial'],
            IMEI=request.POST['IMEI'],
            bateria=request.POST['bateria'],
            observaciones=request.POST['observaciones'],
        )
        equipo.save()
        descripcion = 'Se registra telefono a nombre de: ' + equipo.cliente.cedula + 'marca:' + request.POST['marca'] + 'modelo:' + request.POST['modelo'] + 'serial:' + request.POST['serial'] + 'IMEI:' + request.POST['IMEI'] + 'bateria:' + request.POST['bateria'] + 'observaciones:' + request.POST['observaciones']
    if descripcion != '':
        bitacora = Bitacora(
            tipo=tipo,
            object_id=equipo.id,
            accion='1',
            user=request.user,
            descripcion=descripcion
        )
        bitacora.save()
    result = json.dumps('reguistrado', ensure_ascii=False)
    return HttpResponse(result, content_type='application/json; charset=utf-8')


def lista_clientes(request):
    clientes = Clientes.objects.all()
    return render(request, 'lista_clientes.html', {'clientes': clientes,})


def lista_user(request):
    user = User.objects.exclude(id=request.user.id)
    return render(request, 'lista_user.html', {'user': user,})


def lista_telefonos(request):
    telefonos = Celulares.objects.all()
    clientes = Clientes.objects.all()
    return render(request, 'lista_telefonos.html', {'telefonos': telefonos, 'clientes': clientes,})


def lista_pc(request):
    telefonos = Pc.objects.all()
    clientes = Clientes.objects.all()
    return render(request, 'lista_pc.html', {'telefonos': telefonos, 'clientes': clientes,})


def lista_bitacora(request):
    clientes = Bitacora.objects.all()
    return render(request, 'lista_bitacora.html', {'clientes': clientes,})


def indexAjax(request):
    clientes = Clientes.objects.all()
    return render(request, 'indexAjax.html', {'clientes': clientes,})


def update_cliente(request):
    if request.GET:
        dicc = {}
        lista_telefonos = []
        lista_direcciones = []
        cliente = Clientes.objects.get(id=request.GET['id'])
        telefonos = Telefono.objects.filter(cliente=cliente)
        direcciones = Direccion.objects.filter(cliente=cliente)
        for x in telefonos:
            lista_telefonos.append(x.telefono)
        for x in direcciones:
            lista_direcciones.append(x.direccion)
        dicc = {
            'id': cliente.id,
            'cedula': cliente.cedula,
            'nombre': cliente.nombre,
            'apellido': cliente.apellido,
            'sexo': cliente.sexo,
            'fecha_de_nacimiento': cliente.fecha_de_nacimiento.strftime('%Y-%m-%d'),
            'telefonos': lista_telefonos,
            'direcciones': lista_direcciones,
        }
        result = json.dumps(dicc, ensure_ascii=False)
    if request.POST:
        cli = Clientes.objects.get(id=request.POST['id'])
        cliente = Clientes.objects.filter(id=request.POST['id']).update(
            cedula=request.POST["cedula"],
            nombre=request.POST["nombre"],
            apellido=request.POST["apellido"],
            sexo=request.POST["sexo"],
            fecha_de_nacimiento=request.POST["fecha_de_nacimiento"],
        )
        cliente = Clientes.objects.get(id=request.POST['id'])
        descripcion = ''
        if cli.cedula != request.POST["cedula"]:
            descripcion += "se modifca cedula: " + cli.cedula + ' por: ' + cliente.cedula + ', '
        if cli.nombre != request.POST["nombre"]:
            descripcion += "se modifca nombre: " + cli.nombre + ' por: ' + cliente.nombre + ', '
        if cli.apellido != request.POST["apellido"]:
            descripcion += "se modifca apellido: " + cli.apellido + ' por: ' + cliente.apellido + ', '
        if cli.sexo != request.POST["sexo"]:
            descripcion += "se modifca sexo: " + cli.sexo + ' por: ' + cliente.sexo + ', '
        if cli.fecha_de_nacimiento != request.POST["fecha_de_nacimiento"]:
            descripcion += "se modifca fecha de nacimiento: " + cli.fecha_de_nacimiento.strftime('%Y-%m-%d') + ' por: ' + cliente.fecha_de_nacimiento.strftime('%Y-%m-%d') + ', '
        telefono = Telefono.objects.filter(cliente=request.POST['id'])
        telefono.delete()
        direcciones = Direccion.objects.filter(cliente=request.POST['id'])
        direcciones.delete()
        telefonos = request.POST.getlist('telefonos[]')
        direcciones = request.POST.getlist('direcciones[]')
        aux = 1 
        for x in telefonos:
            if x != '':
                telefono = Telefono(
                    cliente=cliente,
                    telefono=x,
                )
                telefono.save()
                if aux == 1:
                    descripcion += ' telefono(s): ' + x + ', '
                else:
                    descripcion += x + ', ' 
                aux += 1
        aux = 1 
        for x in direcciones:
            if x != '':
                direccion = Direccion(
                    cliente=cliente,
                    direccion=x,
                )
                direccion.save()
                if aux == 1:
                    descripcion += ' direccion(es): ' + x + ', '
                else:
                    descripcion += x + ', '
                aux += 1
        if descripcion != '':
            bitacora = Bitacora(
                tipo='1',
                object_id=cliente.id,
                accion='2',
                user=request.user,
                descripcion=descripcion
            )
            bitacora.save()
        result = json.dumps("Actualizado", ensure_ascii=False)
    return HttpResponse(result, content_type='application/json; charset=utf-8')


def change_password(request):
    if request.method == "POST":
        user = User.objects.get(id=request.POST["id"])
        user.set_password(request.POST["password"])
        user.save()
        if request.user.id != request.POST['id']:
            descripcion = 'El usuario ' + request.user.username + ' le modifico la clave al usuario ' + user.username
        else:
            descripcion = 'El usuario ' + user.username + ' cambio su clave'
        if descripcion != '':
            bitacora = Bitacora(
                tipo='7',
                object_id=user.id,
                accion='2',
                user_id=request.user.id,
                descripcion=descripcion
            )
            bitacora.save()
    return HttpResponse(json.dumps({"message": "password cambiada."}, ensure_ascii=False), content_type='application/json; charset=utf-8')


def update_user(request):
    if request.method == "GET":
        user = User.objects.get(id=request.GET["id"])
        dicc = {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "admistrador": user.is_staff,
        }
    if request.method == "POST":
        user_old = User.objects.get(id=request.POST["id"])
        user = User.objects.get(id=request.POST["id"])
        user.username = request.POST["username"]
        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
        user.email = request.POST["email"]
        tipo = ''
        if request.POST.has_key('tipo'):
            if request.POST['tipo'] == '2':
                user.is_staff = True
                tipo = 'Administrador'
            elif request.POST['tipo'] == '1':
                user.is_staff = False
                tipo = 'Normal'
        user.save()
        dicc = {
            "id": request.POST["id"],
            "username": request.POST["username"],
            "first_name": request.POST["first_name"],
            "last_name": request.POST["last_name"],
            "email": request.POST["email"] ,
        }
        descripcion = ''
        if user_old.username != user.username:
            descripcion += 'Se cambia username: ' + user_old.username + ' por: ' + user.username + ', '
        if user_old.first_name != user.first_name:
            descripcion += 'Se cambia nombre: ' + user_old.first_name + ' por: ' + user.first_name + ', '
        if user_old.last_name != user.last_name:
            descripcion += 'Se cambia apellido: ' + user_old.last_name + ' por: ' + user.last_name + ', '
        if user_old.email != user.email:
            descripcion += 'Se cambia email: ' + user_old.email + ' por: ' + user.email + ', '
        if user_old.is_staff != user.is_staff:
            descripcion += 'Ahora es un usuario de tipo ' + tipo
        if descripcion != '':  
            bitacora = Bitacora(
                tipo='7',
                object_id=user.id,
                accion='2',
                user=request.user,
                descripcion=descripcion
            )
            bitacora.save()
    return HttpResponse(json.dumps(dicc, ensure_ascii=False), content_type='application/json; charset=utf-8')


def revisar_cedula(request):
    if Clientes.objects.filter(cedula=request.GET['cedula']).exists():
        resp = True
    else:
        resp = False
    return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type='application/json; charset=utf-8')  


def restaurar_super_user(request):
    user = User.objects.get(id=1)
    user.set_password('123')
    user.save()
    return HttpResponse(json.dumps(user.username, ensure_ascii=False), content_type='application/json; charset=utf-8')        


def update_phone(request):
    if request.GET:
        dicc = {}
        telefono = Celulares.objects.get(id=request.GET['id'])
        dicc = {
            'id': telefono.id,
            'cliente': telefono.cliente.id,
            'marca': telefono.marca,
            'modelo': telefono.modelo,
            'serial': telefono.serial,
            'IMEI': telefono.IMEI,
            'bateria': telefono.bateria,
            'observaciones': telefono.observaciones,
        }
        result = json.dumps(dicc, ensure_ascii=False)
    if request.POST:
        telefono_old = Celulares.objects.get(id=request.POST['id'])
        telefono = Celulares.objects.filter(id=request.POST['id']).update(
            cliente_id=request.POST['cliente'],
            marca=request.POST['marca'],
            modelo=request.POST['modelo'],
            serial=request.POST['serial'],
            IMEI=request.POST['IMEI'],
            bateria=request.POST['bateria'],
            observaciones=request.POST['observaciones'],
        )
        telefono = Celulares.objects.get(id=request.POST['id'])
        descripcion = ''
        if telefono.cliente != telefono_old.cliente:
            descripcion += 'Se cambia cliente: ' + telefono_old.cliente.cedula + ' por: ' + telefono.cliente.cedula
        if telefono.marca != telefono_old.marca:
            descripcion += 'Se cambia marca: ' + telefono_old.marca + ' por: ' + telefono.marca
        if telefono.modelo != telefono_old.modelo:
            descripcion += 'Se cambia modelo: ' + telefono_old.modelo + ' por: ' + telefono.modelo
        if telefono.serial != telefono_old.serial:
            descripcion += 'Se cambia serial: ' + telefono_old.serial + ' por: ' + telefono.serial
        if telefono.IMEI != telefono_old.IMEI:
            descripcion += 'Se cambia IMEI: ' + telefono_old.IMEI + ' por: ' + telefono.IMEI
        if telefono.bateria != telefono_old.bateria:
            descripcion += 'Se cambia bateria: ' + telefono_old.bateria + ' por: ' + telefono.bateria
        if telefono.observaciones != telefono_old.observaciones:
            descripcion += 'Se cambia observaciones: ' + telefono_old.observaciones + ' por: ' + telefono.observaciones
        if descripcion != '':
            bitacora = Bitacora(
                tipo='7',
                object_id=user.id,
                accion='2',
                user=request.user,
                descripcion=descripcion
            )
            bitacora.save()
        result = json.dumps("Actualizado", ensure_ascii=False)
    return HttpResponse(result, content_type='application/json; charset=utf-8')


def update_pc(request):
    if request.GET:
        dicc = {}
        pc = Pc.objects.get(id=request.GET['id'])
        dicc = {
            'id': pc.id,
            'cliente': pc.cliente.id,
            'marca': pc.marca,
            'modelo': pc.modelo,
            'HDD': pc.HDD,
            'tarjeta_madre': pc.tarjeta_madre,
            'CPU': pc.CPU,
            'RAM': pc.RAM,
            'unida_DVD': pc.unida_DVD,
            'fuente_de_poder': pc.fuente_de_poder,
            'observaciones': pc.observaciones,
        }
        result = json.dumps(dicc, ensure_ascii=False)
    if request.POST:
        pc_old = Pc.objects.get(id=request.POST['id'])
        pc = Pc.objects.filter(id=request.POST['id']).update(
            cliente_id=request.POST['cliente'],
            marca=request.POST['marca'],
            modelo=request.POST['modelo'],
            HDD=request.POST['HDD'],
            tarjeta_madre=request.POST['tarjeta_madre'],
            CPU=request.POST['CPU'],
            RAM=request.POST['RAM'],
            unida_DVD=request.POST['unida_DVD'],
            fuente_de_poder=request.POST['fuente_de_poder'],
            observaciones=request.POST['observaciones'],
        )
        pc = Pc.objects.get(id=request.POST['id'])
        descripcion = ''
        if pc_old.cliente_id != pc.cliente_id:
            descripcion += 'Se cambia cliente_id:' + pc_old.cliente.cedula + ' por: ' + pc.cliente.cedula
        if pc_old.marca != pc.marca:
            descripcion += 'Se cambia marca:' + pc_old.marca + ' por: ' + pc.marca
        if pc_old.modelo != pc.modelo:
            descripcion += 'Se cambia modelo:' + pc_old.modelo + ' por: ' + pc.modelo
        if pc_old.HDD != pc.HDD:
            descripcion += 'Se cambia HDD:' + pc_old.HDD + ' por: ' + pc.HDD
        if pc_old.tarjeta_madre != pc.tarjeta_madre:
            descripcion += 'Se cambia tarjeta madre:' + pc_old.tarjeta_madre + ' por: ' + pc.tarjeta_madre
        if pc_old.CPU != pc.CPU:
            descripcion += 'Se cambia CPU:' + pc_old.CPU + ' por: ' + pc.CPU
        if pc_old.RAM != pc.RAM:
            descripcion += 'Se cambia RAM:' + pc_old.RAM + ' por: ' + pc.RAM
        if pc_old.unida_DVD != pc.unida_DVD:
            descripcion += 'Se cambia unida DVD:' + pc_old.unida_DVD + ' por: ' + pc.unida_DVD
        if pc_old.fuente_de_poder != pc.fuente_de_poder:
            descripcion += 'Se cambia fuente de poder:' + pc_old.fuente_de_poder + ' por: ' + pc.fuente_de_poder
        if pc_old.observaciones != pc.observaciones:
            descripcion += 'Se cambia observaciones:' + pc_old.observaciones + ' por: ' + pc.observaciones
        if descripcion != '':
            bitacora = Bitacora(
                tipo='7',
                object_id=user.id,
                accion='2',
                user=request.user,
                descripcion=descripcion
            )
            bitacora.save()
        result = json.dumps("Actualizado", ensure_ascii=False)
    return HttpResponse(result, content_type='application/json; charset=utf-8')


def create_user(request):
    if request.method == "POST":
        user = User()
        user.username = request.POST["username"]
        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
        user.email = request.POST["email"]
        user.set_password(request.POST["email"])
        if request.POST['tipo'] == '2':
            user.is_staff = True
        elif request.POST['tipo'] == '1':
            user.is_staff = False
        user.save()
        dicc = {}
        bitacora = Bitacora(
            tipo='7',
            object_id=user.id,
            accion='1',
            user=request.user,
            descripcion='Se registra al usuarios: ' + request.POST["username"] + ', ' + 'nombre: ' + request.POST["first_name"] + ', ' + 'apellido: ' + request.POST["last_name"] + ', ' + 'email: ' + request.POST["email"] + ', '
        )
        bitacora.save()
    return HttpResponse(json.dumps(dicc, ensure_ascii=False), content_type='application/json; charset=utf-8')