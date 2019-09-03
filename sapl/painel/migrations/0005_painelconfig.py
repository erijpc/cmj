# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-06-10 11:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('painel', '0004_auto_20190603_1033'),
    ]

    operations = [
        migrations.CreateModel(
            name='PainelConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cronometro_ordem', models.BooleanField(choices=[(True, 'Sim'), (False, 'Não')], default=True, verbose_name='Cronômetro da Questão de Ordem deve travar os demais?')),
            ],
            options={
                'verbose_name': 'Configurações do Painel',
                'verbose_name_plural': 'Configurações do Painel',
                'ordering': ('-id',),
            },
        ),
    ]
