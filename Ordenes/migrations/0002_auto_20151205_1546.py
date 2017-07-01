# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Clientes', '0002_celulares_pc'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Ordenes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrdenesCompletar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('diagnostico', models.TextField()),
                ('fecha_de_culminacion', models.DateTimeField()),
                ('fecha_de_creacion', models.DateTimeField(auto_now_add=True)),
                ('observaciones', models.TextField()),
                ('garantia', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'ordenes_completadas',
            },
        ),
        migrations.CreateModel(
            name='OrdenesEntragadas',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_de_entrega', models.DateTimeField()),
                ('fecha_de_creacion', models.DateTimeField(auto_now_add=True)),
                ('clientes', models.ForeignKey(to='Clientes.Clientes')),
                ('orden', models.ForeignKey(to='Ordenes.OrdenesCompletar')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'entrega_ordenes',
            },
        ),
        migrations.AddField(
            model_name='ordenes',
            name='descripcion',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='ordenes',
            name='observaciones',
            field=models.TextField(default='hola'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ordenescompletar',
            name='orden',
            field=models.ForeignKey(to='Ordenes.Ordenes'),
        ),
        migrations.AddField(
            model_name='ordenescompletar',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
