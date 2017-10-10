# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-10-10 17:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parlamentares', '0010_corrige_data_inicio_mandato'),
        ('sigad', '0017_auto_20171006_1255'),
    ]

    operations = [
        migrations.AddField(
            model_name='classe',
            name='parlamentar',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='classe_set', to='parlamentares.Parlamentar', verbose_name='Parlamentar'),
        ),
        migrations.AlterField(
            model_name='classe',
            name='template_classe',
            field=models.IntegerField(choices=[(1, 'Listagem Simples em Linha'), (2, 'Galeria Pública de Albuns'), (3, 'Página dos Parlamentares'), (4, 'Página individual de Parlamentar')], default=1, verbose_name='Template para a Classe'),
        ),
    ]
