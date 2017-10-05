# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-08-17 17:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sigad', '0004_auto_20170816_1103'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferenciaEntreDocumentos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordem', models.IntegerField(default=0, verbose_name='Ordem de Renderização')),
            ],
        ),
        migrations.AlterField(
            model_name='classe',
            name='visibilidade',
            field=models.IntegerField(choices=[(2, 'Restrição por Permissão'), (1, 'Restrição por Usuário'), (99, 'Privado'), (0, 'Público')], default=99, verbose_name='Visibilidade'),
        ),
        migrations.AlterField(
            model_name='documento',
            name='tipo',
            field=models.IntegerField(choices=[(100, 'Texto'), (800, 'Vídeo'), (700, 'Container'), (900, 'Imagem')], default=0, verbose_name='Tipo da Parte do Documento'),
        ),
        migrations.AlterField(
            model_name='documento',
            name='visibilidade',
            field=models.IntegerField(choices=[(2, 'Restrição por Permissão'), (1, 'Restrição por Usuário'), (99, 'Privado'), (0, 'Público')], default=99, verbose_name='Visibilidade'),
        ),
        migrations.AlterField(
            model_name='permissionsuserclasse',
            name='visibilidade',
            field=models.IntegerField(choices=[(2, 'Restrição por Permissão'), (1, 'Restrição por Usuário'), (99, 'Privado'), (0, 'Público')], default=99, verbose_name='Visibilidade'),
        ),
        migrations.AlterField(
            model_name='permissionsuserdocumento',
            name='visibilidade',
            field=models.IntegerField(choices=[(2, 'Restrição por Permissão'), (1, 'Restrição por Usuário'), (99, 'Privado'), (0, 'Público')], default=99, verbose_name='Visibilidade'),
        ),
        migrations.AlterField(
            model_name='revisao',
            name='visibilidade',
            field=models.IntegerField(blank=True, choices=[(2, 'Restrição por Permissão'), (1, 'Restrição por Usuário'), (99, 'Privado'), (0, 'Público')], default=None, null=True, verbose_name='Visibilidade'),
        ),
        migrations.AddField(
            model_name='referenciaentredocumentos',
            name='referenciado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='referenciado', to='sigad.Documento', verbose_name='Documento Referenciado'),
        ),
        migrations.AddField(
            model_name='referenciaentredocumentos',
            name='referente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='referente', to='sigad.Documento', verbose_name='Documento Referente'),
        ),
        migrations.AddField(
            model_name='documento',
            name='referencias',
            field=models.ManyToManyField(through='sigad.ReferenciaEntreDocumentos', to='sigad.Documento'),
        ),
    ]
