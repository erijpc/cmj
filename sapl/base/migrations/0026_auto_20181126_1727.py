# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-11-26 19:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0025_auto_20181126_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appconfig',
            name='cronometro_discurso',
            field=models.DurationField(blank=True, null=True, verbose_name='Cronômetro do Discurso'),
        ),
    ]
