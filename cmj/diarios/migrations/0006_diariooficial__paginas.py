# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-02-19 13:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diarios', '0005_auto_20190916_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='diariooficial',
            name='_paginas',
            field=models.IntegerField(default=0, verbose_name='Número de Páginas'),
        ),
    ]
