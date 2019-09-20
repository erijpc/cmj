# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2019-09-20 13:45
from __future__ import unicode_literals

import cmj.core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('core', '0019_auto_20190917_2256'),
    ]

    operations = [
        migrations.CreateModel(
            name='CertidaoPublicacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('object_id', models.PositiveIntegerField(blank=True, default=None, null=True)),
                ('hash_code', models.CharField(blank=True, max_length=200, verbose_name='Hash de Publicação')),
                ('cancelado', models.BooleanField(choices=[(True, 'Sim'), (False, 'Não')], default=False, verbose_name='Cancelado ')),
                ('content_type', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('modifier', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='modifier')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
            options={
                'abstract': False,
            },
            bases=(cmj.core.models.CmjCleanMixin, models.Model),
        ),
    ]
