# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-03-30 18:06
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
import django.core.serializers.json
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('protocoloadm', '0045_protocolo_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentoadministrativo',
            name='metadata',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=None, encoder=django.core.serializers.json.DjangoJSONEncoder, null=True, verbose_name='Metadados'),
        ),
    ]
