# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-22 16:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0004_tipoevento'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='tipo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='agenda.TipoEvento', verbose_name='Tipo de Evento'),
            preserve_default=False,
        ),
    ]
