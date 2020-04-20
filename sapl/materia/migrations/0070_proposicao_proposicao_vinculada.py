# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-04-14 11:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('materia', '0069_tipoproposicao_tipo_autores'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposicao',
            name='proposicao_vinculada',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='proposicao_vinculada_set', to='materia.Proposicao', verbose_name='Proposição Vinculada'),
        ),
    ]