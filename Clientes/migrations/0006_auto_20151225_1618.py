# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Clientes', '0005_auto_20151225_0754'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='celulares',
            name='observaciones',
        ),
        migrations.AddField(
            model_name='bitacora',
            name='fecha_de_creacion',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 25, 20, 48, 38, 663405, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bitacora',
            name='tipo',
            field=models.CharField(blank=True, max_length=2, null=True, choices=[(b'1', b'Clientes'), (b'2', b'Pc'), (b'3', b'Telefono'), (b'4', b'Peticiones'), (b'5', b'Peticiones Completadas'), (b'6', b'Peticiones Entregadas'), (b'7', b'Usuarios')]),
        ),
    ]
