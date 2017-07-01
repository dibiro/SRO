# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ordenes', '0004_auto_20151206_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordenes',
            name='estado',
            field=models.CharField(default=b'1', max_length=2, choices=[(b'1', b'Recibido'), (b'2', b'Cumplido'), (b'3', b'Entregado'), (b'4', b'Anuladas')]),
        ),
    ]
