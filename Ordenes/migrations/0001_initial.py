# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ordenes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.BigIntegerField()),
                ('tipo', models.CharField(blank=True, max_length=2, null=True, choices=[(b'1', b'Celulares'), (b'2', b'Pc')])),
                ('estado', models.CharField(default=b'1', max_length=2, choices=[(b'1', b'Recibido'), (b'2', b'Cumplido'), (b'3', b'Entregado')])),
                ('fecha_de_recibido', models.DateTimeField()),
                ('fecha_de_creacion', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ordenes',
            },
        ),
    ]
