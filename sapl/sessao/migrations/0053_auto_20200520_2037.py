# Generated by Django 2.2.12 on 2020-05-20 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sessao', '0052_auto_20200512_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessaoplenaria',
            name='painel_aberto',
            field=models.BooleanField(blank=True, default=False, verbose_name='Painel está aberto?'),
        ),
    ]
