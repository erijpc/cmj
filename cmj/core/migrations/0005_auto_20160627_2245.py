# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-28 01:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20160627_2234'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='trecho',
            options={'ordering': ['municipio__nome', 'regiao_municipal__nome', 'distrito__nome', 'bairro__nome', 'logradouro__nome'], 'permissions': (('search_trecho', 'Consultar base de Trechos.'),), 'verbose_name': 'Trecho de Logradouro', 'verbose_name_plural': 'Trechos de Logradouro'},
        ),
    ]
