# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-03-25 03:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_auto_20200221_1426'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bi',
            options={'ordering': ('-id', '-ano', 'content_type'), 'verbose_name': 'Bi', 'verbose_name_plural': 'Bi'},
        ),
    ]
