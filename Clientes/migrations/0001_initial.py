# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clientes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cedula', models.CharField(max_length=50)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('sexo', models.CharField(blank=True, max_length=2, null=True, choices=[(b'1', b'Masculino'), (b'2', b'Femenino')])),
                ('fecha_de_nacimiento', models.DateField(null=True, blank=True)),
            ],
            options={
                'db_table': 'clientes',
            },
        ),
        migrations.CreateModel(
            name='Direccion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('direccion', models.TextField()),
                ('cliente', models.ForeignKey(to='Clientes.Clientes')),
            ],
            options={
                'db_table': 'direccion',
            },
        ),
        migrations.CreateModel(
            name='Telefono',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('telefono', models.CharField(max_length=50)),
                ('cliente', models.ForeignKey(to='Clientes.Clientes')),
            ],
            options={
                'db_table': 'telefono',
            },
        ),
    ]
