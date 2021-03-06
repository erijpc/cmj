from django.contrib.postgres.fields.jsonb import JSONField
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.translation import ugettext_lazy as _
import reversion

from cmj.mixins import CountPageMixin
from cmj.utils import texto_upload_path
from sapl.norma.models import NormaJuridica
from sapl.utils import restringe_tipos_de_arquivo_txt, OverwriteStorage


@reversion.register()
class TipoDeDiario(models.Model):
    descricao = models.CharField(max_length=50, verbose_name=_('Descrição'))

    class Meta:
        verbose_name = _('Tipo de Diário')
        verbose_name_plural = _('Tipos de Diário')

    def __str__(self):
        return self.descricao


def diario_upload_path(instance, filename):
    return texto_upload_path(instance, filename, subpath=instance.ano)


@reversion.register()
class DiarioOficial(CountPageMixin):
    FIELDFILE_NAME = ('arquivo', )

    metadata = JSONField(
        verbose_name=_('Metadados'),
        blank=True, null=True, default=None, encoder=DjangoJSONEncoder)

    edicao = models.PositiveIntegerField(
        default=0,
        verbose_name='Edição')

    descricao = models.CharField(max_length=250, verbose_name=_('Descrição'))

    tipo = models.ForeignKey(
        TipoDeDiario,
        on_delete=models.PROTECT,
        verbose_name=_('Tipo do Diário'))

    data = models.DateField(
        blank=True, null=True, verbose_name=_('Data'))

    arquivo = models.FileField(
        blank=True,
        null=True,
        upload_to=diario_upload_path,
        storage=OverwriteStorage(),
        verbose_name=_('Arquivo Digital do Diário'),
        validators=[restringe_tipos_de_arquivo_txt])

    normas = models.ManyToManyField(
        NormaJuridica,
        verbose_name=_('Normas Publicadas no Diário'))

    data_ultima_atualizacao = models.DateTimeField(
        blank=True, null=True,
        auto_now=True,
        verbose_name=_('Data'))

    class Meta:
        verbose_name = _('Diário Oficial')
        verbose_name_plural = _('Diários Oficiais')
        ordering = ('-data', 'edicao')

    def __str__(self):
        return self.descricao

    @property
    def ano(self):
        return self.data.year

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if not self.pk and self.arquivo:
            arquivo = self.arquivo
            self.arquivo = None
            models.Model.save(self, force_insert=force_insert,
                              force_update=force_update,
                              using=using,
                              update_fields=update_fields)
            self.arquivo = arquivo

        return models.Model.save(self, force_insert=force_insert,
                                 force_update=force_update,
                                 using=using,
                                 update_fields=update_fields)
