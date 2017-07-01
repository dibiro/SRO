# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Clientes', '0002_celulares_pc'),
        ('Ordenes', '0003_auto_20151205_1548'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ordenesentragadas',
            old_name='clientes',
            new_name='cliente',
        ),
        migrations.AddField(
            model_name='ordenes',
            name='cliente',
            field=models.ForeignKey(default=1, to='Clientes.Clientes'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ordenes',
            name='tipo',
            field=models.CharField(blank=True, max_length=2, null=True, choices=[(b'1', b'Pc'), (b'2', b'Celulares')]),
        ),
    ]
