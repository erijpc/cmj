# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2019-09-19 21:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('protocoloadm', '0037_documentoadministrativo_epigrafe'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tramitacaoadministrativo',
            options={'ordering': ('-data_tramitacao', '-id'), 'verbose_name': 'Tramitação de Documento Administrativo', 'verbose_name_plural': 'Tramitações de Documento Administrativo'},
        ),
    ]