# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Clientes', '0002_celulares_pc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientes',
            name='cedula',
            field=models.CharField(unique=True, max_length=50),
        ),
    ]
