# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-04-10 14:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sigad', '0036_auto_20180216_1553'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='caixapublicacao',
            name='documentos',
        ),
    ]
