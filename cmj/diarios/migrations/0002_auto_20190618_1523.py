# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-06-18 18:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('norma', '0024_auto_20190425_0917'),
        ('diarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='diariooficial',
            options={'ordering': ('-data',), 'verbose_name': 'Diário Oficial', 'verbose_name_plural': 'Diários Oficiais'},
        ),
        migrations.AddField(
            model_name='diariooficial',
            name='normas',
            field=models.ManyToManyField(to='norma.NormaJuridica'),
        ),
    ]
