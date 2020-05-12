# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-05-05 18:51
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
import django.core.serializers.json
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ouvidoria', '0010_auto_20200329_0939'),
    ]

    operations = [
        migrations.AddField(
            model_name='mensagemsolicitacao',
            name='metadata',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=None, encoder=django.core.serializers.json.DjangoJSONEncoder, null=True, verbose_name='Metadados'),
        ),
    ]