# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-31 14:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parlamentares', '0030_auto_20190531_0848'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='partido',
            options={'ordering': ['sigla', 'nome'], 'verbose_name': 'Partido', 'verbose_name_plural': 'Partidos'},
        ),
    ]
