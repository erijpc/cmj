# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2019-10-15 13:19
from __future__ import unicode_literals

import cmj.utils
from django.db import migrations, models
import sapl.norma.models
import sapl.utils


class Migration(migrations.Migration):

    dependencies = [
        ('norma', '0027_merge_20190802_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anexonormajuridica',
            name='anexo_arquivo',
            field=models.FileField(blank=True, null=True, storage=sapl.utils.OverwriteStorage(), upload_to=sapl.norma.models.norma_upload_path, validators=[cmj.utils.restringe_tipos_de_arquivo_midias], verbose_name='Arquivo Anexo'),
        ),
    ]
