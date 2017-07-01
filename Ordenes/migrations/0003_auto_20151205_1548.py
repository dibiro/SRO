# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ordenes', '0002_auto_20151205_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordenes',
            name='descripcion',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
