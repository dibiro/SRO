# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Clientes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Celulares',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('marca', models.CharField(max_length=50)),
                ('modelo', models.CharField(max_length=50)),
                ('serial', models.CharField(max_length=50)),
                ('IMEI', models.CharField(max_length=15)),
                ('bateria', models.CharField(max_length=50, null=True, blank=True)),
                ('observaciones', models.TextField()),
                ('cliente', models.ForeignKey(to='Clientes.Clientes')),
            ],
            options={
                'db_table': 'celulares',
            },
        ),
        migrations.CreateModel(
            name='Pc',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('marca', models.CharField(max_length=50)),
                ('modelo', models.CharField(max_length=50)),
                ('HDD', models.CharField(max_length=50)),
                ('tarjeta_madre', models.CharField(max_length=50)),
                ('CPU', models.CharField(max_length=50, null=True, blank=True)),
                ('RAM', models.CharField(max_length=50, null=True, blank=True)),
                ('unida_DVD', models.CharField(max_length=50, null=True, blank=True)),
                ('fuente_de_poder', models.CharField(max_length=50, null=True, blank=True)),
                ('observaciones', models.TextField()),
                ('cliente', models.ForeignKey(to='Clientes.Clientes')),
            ],
            options={
                'db_table': 'pc',
            },
        ),
    ]
