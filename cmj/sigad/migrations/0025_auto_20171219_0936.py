# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-19 11:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sigad', '0024_classe_tipo_doc_padrao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classe',
            name='tipo_doc_padrao',
            field=models.IntegerField(choices=[(0, 'Documento'), (10, 'Banco de Imagem'), (20, 'Galeria Pública')], default=0, verbose_name='Tipo Padrão para Documentos desta Classe'),
        ),
    ]
