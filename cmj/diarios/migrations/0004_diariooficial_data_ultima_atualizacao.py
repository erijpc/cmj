# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-08-09 16:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diarios', '0003_auto_20190704_2232'),
    ]

    operations = [
        migrations.AddField(
            model_name='diariooficial',
            name='data_ultima_atualizacao',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Data'),
        ),
    ]