# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-19 17:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0006_auto_20180619_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='caracteristica',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Eventos Diversos'), (1, 'Feriado')], default=0, verbose_name='Caracteristica?'),
        ),
    ]
