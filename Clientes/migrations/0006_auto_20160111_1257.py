# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Clientes', '0005_auto_20151225_0754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bitacora',
            name='tipo',
            field=models.CharField(blank=True, max_length=2, null=True, choices=[(b'1', b'Clientes'), (b'2', b'Pc'), (b'3', b'Telefono'), (b'4', b'Peticiones'), (b'5', b'Peticiones Completadas'), (b'6', b'Peticiones Entregadas'), (b'7', b'Usuarios')]),
        ),
    ]
