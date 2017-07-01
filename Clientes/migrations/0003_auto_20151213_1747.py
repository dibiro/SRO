# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Clientes', '0002_celulares_pc'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bitacora',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo', models.CharField(blank=True, max_length=2, null=True, choices=[(b'1', b'Clientes'), (b'2', b'Pc'), (b'3', b'Telefono'), (b'4', b'Peticiones'), (b'5', b'Peticiones Completadas'), (b'6', b'Peticiones Entregadas')])),
                ('object_id', models.BigIntegerField()),
                ('accion', models.PositiveIntegerField()),
                ('descripcion', models.TextField()),
            ],
            options={
                'db_table': 'bitacora',
            },
        ),
        migrations.AlterField(
            model_name='clientes',
            name='cedula',
            field=models.CharField(unique=True, max_length=50),
        ),
    ]
