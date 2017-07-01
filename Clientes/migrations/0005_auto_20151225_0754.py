# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Clientes', '0004_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='bitacora',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bitacora',
            name='accion',
            field=models.CharField(blank=True, max_length=2, null=True, choices=[(b'1', b'Crear'), (b'2', b'Modificar'), (b'3', b'Elimina')]),
        ),
    ]
