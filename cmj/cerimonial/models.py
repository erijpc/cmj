
from compressor.utils.decorators import cached_property
from django.contrib.auth.models import Group
from django.db import models
from django.db.models.deletion import SET_NULL, PROTECT, CASCADE
from django.utils.translation import ugettext_lazy as _
from sapl.parlamentares.models import Parlamentar, Municipio, Partido
from sapl.utils import UF

from cmj.core.models import CmjModelMixin, Trecho, Distrito, RegiaoMunicipal,\
    CmjAuditoriaModelMixin, CmjSearchMixin
from cmj.utils import YES_NO_CHOICES, NONE_YES_NO_CHOICES,\
    get_settings_auth_user_model


FEMININO = 'F'
MASCULINO = 'M'
SEXO_CHOICE = ((FEMININO, _('Feminino')),
               (MASCULINO, _('Masculino')))


class DescricaoAbstractModel(models.Model):
    descricao = models.CharField(
        default='', max_length=254, verbose_name=_('Nome / Descrição'))

    class Meta:
        abstract = True

    def __str__(self):
        return self.descricao


class StatusVisita(DescricaoAbstractModel):

    class Meta:
        verbose_name = _('Status da Visita')
        verbose_name_plural = _('Status das Visitas')


class TipoTelefone(DescricaoAbstractModel):

    class Meta:
        verbose_name = _('Tipo de Telefone')
        verbose_name_plural = _('Tipos de Telefone')


class TipoEndereco(DescricaoAbstractModel):

    class Meta:
        verbose_name = _('Tipo de Endereço')
        verbose_name_plural = _('Tipos de Endereço')


class TipoEmail(DescricaoAbstractModel):

    class Meta:
        verbose_name = _('Tipo de Email')
        verbose_name_plural = _('Tipos de Email')


class Parentesco(DescricaoAbstractModel):

    class Meta:
        verbose_name = _('Parentesco')
        verbose_name_plural = _('Parentescos')


class EstadoCivil(DescricaoAbstractModel):

    class Meta:
        verbose_name = _('Estado Civil')
        verbose_name_plural = _('Estados Civis')


class PronomeTratamento(models.Model):

    nome_por_extenso = models.CharField(
        default='', max_length=254, verbose_name=_('Nome Por Extenso'))

    abreviatura_singular_m = models.CharField(
        default='', max_length=254, verbose_name=_(
            'Abreviatura Singular Masculino'))

    abreviatura_singular_f = models.CharField(
        default='', max_length=254, verbose_name=_(
            'Abreviatura Singular Feminino'))

    abreviatura_plural_m = models.CharField(
        default='', max_length=254, verbose_name=_(
            'Abreviatura Plural Masculino'))

    abreviatura_plural_f = models.CharField(
        default='', max_length=254, verbose_name=_(
            'Abreviatura Plural Feminino'))

    vocativo_direto_singular_m = models.CharField(
        default='', max_length=254, verbose_name=_(
            'Vocativo Direto Singular Masculino'))

    vocativo_direto_singular_f = models.CharField(
        default='', max_length=254, verbose_name=_(
            'Vocativo Direto Singular Feminino'))

    vocativo_direto_plural_m = models.CharField(
        default='', max_length=254, verbose_name=_(
            'Vocativo Direto Plural Masculino'))

    vocativo_direto_plural_f = models.CharField(
        default='', max_length=254, verbose_name=_(
            'Vocativo Direto Plural Feminino'))

    vocativo_indireto_singular_m = models.CharField(
        default='', max_length=254, verbose_name=_(
            'Vocativo Indireto Singular Masculino'))

    vocativo_indireto_singular_f = models.CharField(
        default='', max_length=254, verbose_name=_(
            'Vocativo Indireto Singular Feminino'))

    vocativo_indireto_plural_m = models.CharField(
        default='', max_length=254, verbose_name=_(
            'Vocativo Indireto Plural Masculino'))

    vocativo_indireto_plural_f = models.CharField(
        default='', max_length=254, verbose_name=_(
            'Vocativo Indireto Plural Feminino'))

    enderecamento_singular_m = models.CharField(
        default='', max_length=254, verbose_name=_(
            'Endereçamento Singular Masculino'))

    enderecamento_singular_f = models.CharField(
        default='', max_length=254, verbose_name=_(
            'Endereçamento Singular Feminino'))

    enderecamento_plural_m = models.CharField(
        default='', max_length=254, verbose_name=_(
            'Endereçamento Plural Masculino'))

    enderecamento_plural_f = models.CharField(
        default='', max_length=254, verbose_name=_(
            'Endereçamento Plural Feminino'))

    class Meta:
        verbose_name = _('Pronome de Tratamento')
        verbose_name_plural = _('Pronomes de tratamento')

    def __str__(self):
        return self.nome_por_extenso


class TipoAutoridade(DescricaoAbstractModel):

    pronomes = models.ManyToManyField(
        PronomeTratamento,
        related_name='tipoautoridade_set')

    class Meta:
        verbose_name = _('Tipo de Autoridade')
        verbose_name_plural = _('Tipos de Autoridade')


class TipoLocalTrabalho(DescricaoAbstractModel):

    class Meta:
        verbose_name = _('Tipo do Local de Trabalho')
        verbose_name_plural = _('Tipos de Local de Trabalho')


class NivelInstrucao(DescricaoAbstractModel):

    class Meta:
        verbose_name = _('Nível de Instrução')
        verbose_name_plural = _('Níveis de Instrução')


class OperadoraTelefonia(DescricaoAbstractModel):

    class Meta:
        verbose_name = _('Operadora de Telefonia')
        verbose_name_plural = _('Operadoras de Telefonia')


class AreaTrabalho(CmjAuditoriaModelMixin):

    nome = models.CharField(max_length=100, blank=True, default='',
                            verbose_name=_('Nome'))

    descricao = models.CharField(
        default='', max_length=254, verbose_name=_('Descrição'))

    parlamentar = models.ForeignKey(
        Parlamentar,
        verbose_name=_('Parlamentar'),
        related_name='areatrabalho_set',
        blank=True, null=True, on_delete=CASCADE)

    operadores = models.ManyToManyField(
        get_settings_auth_user_model(),
        through='OperadorAreaTrabalho',
        through_fields=('areatrabalho', 'user'),
        symmetrical=False,
        related_name='areatrabalho_set')

    class Meta:
        verbose_name = _('Área de Trabalho')
        verbose_name_plural = _('Áreas de Trabalho')

    def __str__(self):
        return self.nome


class OperadorAreaTrabalho(CmjAuditoriaModelMixin):

    user = models.ForeignKey(
        get_settings_auth_user_model(),
        verbose_name=_('Operador da Área de Trabalho'),
        related_name='operadorareatrabalho_set',
        on_delete=CASCADE)

    areatrabalho = models.ForeignKey(
        AreaTrabalho,
        related_name='operadorareatrabalho_set',
        verbose_name=_('Área de Trabalho'),
        on_delete=CASCADE)

    grupos_associados = models.ManyToManyField(
        Group,
        verbose_name=_('Grupos Associados'),
        related_name='operadorareatrabalho_set')

    @property
    def user_name(self):
        return '%s - %s' % (
            self.user.get_display_name(),
            self.user.email)

    class Meta:
        verbose_name = _('Operador')
        verbose_name_plural = _('Operadores')

    def __str__(self):
        return self.user.get_display_name()


class Contato(CmjSearchMixin, CmjModelMixin):

    nome = models.CharField(max_length=100, verbose_name=_('Nome'))

    nome_social = models.CharField(
        blank=True, default='', max_length=100, verbose_name=_('Nome Social'))

    apelido = models.CharField(
        blank=True, default='', max_length=100, verbose_name=_('Apelido'))

    data_nascimento = models.DateField(
        blank=True, null=True, verbose_name=_('Data de Nascimento'))

    sexo = models.CharField(
        max_length=1, blank=True,
        verbose_name=_('Sexo Biológico'), choices=SEXO_CHOICE)

    identidade_genero = models.CharField(
        blank=True, default='',
        max_length=100, verbose_name=_('Como se reconhece?'))

    tem_filhos = models.NullBooleanField(
        choices=NONE_YES_NO_CHOICES,
        default=None, verbose_name=_('Tem Filhos?'))

    quantos_filhos = models.PositiveSmallIntegerField(
        default=0,  blank=True, verbose_name=_('Quantos Filhos?'))

    estado_civil = models.ForeignKey(
        EstadoCivil,
        related_name='contato_set',
        blank=True, null=True, on_delete=SET_NULL,
        verbose_name=_('Estado Civil'))

    nivel_instrucao = models.ForeignKey(
        NivelInstrucao,
        related_name='contato_set',
        blank=True, null=True, on_delete=SET_NULL,
        verbose_name=_('Nivel de Instrução'))

    naturalidade = models.CharField(
        max_length=50, blank=True, verbose_name=_('Naturalidade'))

    nome_pai = models.CharField(
        max_length=100, blank=True, verbose_name=_('Nome do Pai'))
    nome_mae = models.CharField(
        max_length=100, blank=True, verbose_name=_('Nome da Mãe'))

    numero_sus = models.CharField(
        max_length=100, blank=True, verbose_name=_('Número do SUS'))
    cpf = models.CharField(max_length=15, blank=True, verbose_name=_('CPF'))
    titulo_eleitor = models.CharField(
        max_length=15,
        blank=True,
        verbose_name=_('Título de Eleitor'))
    rg = models.CharField(max_length=30, blank=True, verbose_name=_('RG'))
    rg_orgao_expedidor = models.CharField(
        max_length=20, blank=True, verbose_name=_('Órgão Expedidor'))
    rg_data_expedicao = models.DateField(
        blank=True, null=True, verbose_name=_('Data de Expedição'))

    ativo = models.BooleanField(choices=YES_NO_CHOICES,
                                default=True, verbose_name=_('Ativo?'))

    workspace = models.ForeignKey(
        AreaTrabalho,
        verbose_name=_('Área de Trabalho'),
        related_name='contato_set',
        blank=True, null=True, on_delete=PROTECT)

    perfil_user = models.ForeignKey(
        get_settings_auth_user_model(),
        verbose_name=_('Perfil do Usuário'),
        related_name='contato_set',
        blank=True, null=True, on_delete=CASCADE)

    profissao = models.CharField(
        max_length=254, blank=True, verbose_name=_('Profissão'))

    tipo_autoridade = models.ForeignKey(
        TipoAutoridade,
        verbose_name=TipoAutoridade._meta.verbose_name,
        related_name='contato_set',
        blank=True, null=True, on_delete=SET_NULL)

    cargo = models.CharField(max_length=254, blank=True, default='',
                             verbose_name=_('Cargo/Função'))

    pronome_tratamento = models.ForeignKey(
        PronomeTratamento,
        verbose_name=PronomeTratamento._meta.verbose_name,
        related_name='contato_set',
        blank=True, null=True, on_delete=SET_NULL,
        help_text=_('O pronome de tratamento é opcional, mas será \
        obrigatório caso seja selecionado um tipo de autoridade.'))

    @cached_property
    def fields_search(self):
        return ['nome',
                'nome_social',
                'apelido']

    class Meta:
        verbose_name = _('Contato')
        verbose_name_plural = _('Contatos')
        ordering = ['nome']

    def __str__(self):
        return self.nome


class PerfilManager(models.Manager):

    def for_user(self, user):
        return super(
            PerfilManager, self).get_queryset().get(
            perfil_user=user)


class Perfil(Contato):
    objects = PerfilManager()

    class Meta:
        proxy = True


class Telefone(CmjModelMixin):

    contato = models.ForeignKey(
        Contato, on_delete=CASCADE, verbose_name=_('Contato'))
    operadora = models.ForeignKey(
        OperadoraTelefonia, on_delete=SET_NULL,
        related_name='telefone_set',
        blank=True, null=True,
        verbose_name=OperadoraTelefonia._meta.verbose_name)
    tipo = models.ForeignKey(
        TipoTelefone, on_delete=PROTECT, verbose_name='Tipo')
    ddd = models.CharField(max_length=3, verbose_name='DDD')
    numero = models.CharField(max_length=20, verbose_name='Número')

    proprio = models.BooleanField(choices=YES_NO_CHOICES,
                                  default=True, verbose_name=_('Próprio?'))

    de_quem_e = models.CharField(
        max_length=40, verbose_name='De quem é?', blank=True,
        help_text=_('Se não é próprio, de quem é?'))

    preferencial = models.BooleanField(
        choices=YES_NO_CHOICES,
        default=True, verbose_name=_('Preferêncial?'))

    permissao = models.BooleanField(
        choices=YES_NO_CHOICES,
        default=True, verbose_name=_('Permissão:'),
        help_text=_("Permite que nossa instituição entre em contato \
        com você neste telefone?"))

    @property
    def numero_nome_contato(self):
        return str(self)

    class Meta:
        verbose_name = _('Telefone')
        verbose_name_plural = _('Telefones')

    def __str__(self):
        return '(%s) %s - (%s)' % (self.ddd, self.numero, self.contato.nome)


class TelefonePerfil(Telefone):

    class Meta:
        proxy = True
        verbose_name = _('Telefone do Perfil')
        verbose_name_plural = _('Telefones do Perfil')


class Email(CmjModelMixin):

    contato = models.ForeignKey(
        Contato, on_delete=CASCADE, verbose_name=_('Contato'))
    tipo = models.ForeignKey(
        TipoEmail,
        blank=True, null=True,
        on_delete=PROTECT, verbose_name='Tipo')
    email = models.EmailField(verbose_name='Email')

    preferencial = models.BooleanField(
        choices=YES_NO_CHOICES,
        default=True, verbose_name=_('Preferêncial?'))

    permissao = models.BooleanField(
        choices=YES_NO_CHOICES,
        default=True, verbose_name=_('Permissão:'),
        help_text=_("Permite que nossa instituição envie informações \
        para este email?"))

    class Meta:
        verbose_name = _('Email')
        verbose_name_plural = _("Email's")

    def __str__(self):
        return self.email


class EmailPerfil(Email):

    class Meta:
        proxy = True
        verbose_name = _('Email do Perfil')
        verbose_name_plural = _("Email's do Perfil")


class Dependente(CmjModelMixin):

    parentesco = models.ForeignKey(Parentesco, verbose_name=_('Parentesco'))
    contato = models.ForeignKey(Contato,
                                verbose_name=('Contato'),
                                related_name='dependente_set',
                                on_delete=CASCADE)
    nome = models.CharField(max_length=100, verbose_name=_('Nome'))

    nome_social = models.CharField(
        blank=True, default='', max_length=100, verbose_name=_('Nome Social'))

    apelido = models.CharField(
        blank=True, default='', max_length=100, verbose_name=_('Apelido'))
    sexo = models.CharField(
        blank=True, max_length=1, verbose_name=_('Sexo Biológico'),
        choices=SEXO_CHOICE)
    data_nascimento = models.DateField(
        blank=True, null=True, verbose_name=_('Data Nascimento'))

    identidade_genero = models.CharField(
        blank=True, default='',
        max_length=100, verbose_name=_('Como se reconhece?'))

    nivel_instrucao = models.ForeignKey(
        NivelInstrucao,
        related_name='dependente_set',
        blank=True, null=True, on_delete=SET_NULL,
        verbose_name=_('Nivel de Instrução'))

    parentesco = models.ForeignKey(
        Parentesco,
        related_name='dependente_set',
        blank=True, null=True, on_delete=SET_NULL,
        verbose_name=_('Parentesco'))

    class Meta:
        verbose_name = _('Dependente')
        verbose_name_plural = _('Dependentes')

    def __str__(self):
        return self.nome


class DependentePerfil(Dependente):

    class Meta:
        proxy = True
        verbose_name = _('Dependente do Perfil')
        verbose_name_plural = _('Dependentes do Perfil')


class LocalTrabalho(CmjModelMixin):
    contato = models.ForeignKey(Contato,
                                verbose_name=('Contato'),
                                related_name='localtrabalho_set',
                                on_delete=CASCADE)
    nome = models.CharField(
        max_length=254, verbose_name=_('Nome / Razão Social'))

    nome_social = models.CharField(
        blank=True, default='', max_length=254,
        verbose_name=_('Nome Fantasia'))

    tipo = models.ForeignKey(
        TipoLocalTrabalho,
        related_name='localtrabalho_set',
        blank=True, null=True, on_delete=SET_NULL,
        verbose_name=_('Tipo do Local de Trabalho'))

    trecho = models.ForeignKey(
        Trecho,
        verbose_name=_('Trecho'),
        related_name='localtrabalho_set',
        blank=True, null=True, on_delete=SET_NULL)

    uf = models.CharField(max_length=2, blank=True, choices=UF,
                          verbose_name=_('Estado'))

    municipio = models.ForeignKey(
        Municipio,
        verbose_name=Municipio._meta.verbose_name,
        related_name='localtrabalho_set',
        blank=True, null=True, on_delete=SET_NULL)

    cep = models.CharField(max_length=9, blank=True, default='',
                           verbose_name=_('CEP'))

    endereco = models.CharField(
        max_length=254, blank=True, default='',
        verbose_name=_('Endereço'),
        help_text=_('O campo endereço também é um campo de busca, nele '
                    'você pode digitar qualquer informação, inclusive '
                    'digitar o cep para localizar o endereço, e vice-versa!'))

    numero = models.CharField(max_length=50, blank=True, default='',
                              verbose_name=_('Número'))

    bairro = models.CharField(max_length=254, blank=True, default='',
                              verbose_name=_('Bairro'))
    distrito = models.ForeignKey(
        Distrito,
        verbose_name=Distrito._meta.verbose_name,
        related_name='localtrabalho_set',
        blank=True, null=True, on_delete=SET_NULL)
    regiao_municipal = models.ForeignKey(
        RegiaoMunicipal,
        verbose_name=RegiaoMunicipal._meta.verbose_name,
        related_name='localtrabalho_set',
        blank=True, null=True, on_delete=SET_NULL)

    complemento = models.CharField(max_length=30, blank=True, default='',
                                   verbose_name=_('Complemento'))

    data_inicio = models.DateField(
        blank=True, null=True, verbose_name=_('Data de Início'))

    data_fim = models.DateField(
        blank=True, null=True, verbose_name=_('Data de Fim'))

    preferencial = models.BooleanField(
        choices=YES_NO_CHOICES,
        default=True, verbose_name=_('Preferencial?'))

    cargo = models.CharField(max_length=254, blank=True, default='',
                             verbose_name=_('Cargo/Função'))

    class Meta:
        verbose_name = _('Local de Trabalho')
        verbose_name_plural = _('Locais de Trabalho')

    def __str__(self):
        return self.nome


class LocalTrabalhoPerfil(LocalTrabalho):

    class Meta:
        proxy = True
        verbose_name = _('Local de Trabalho do Perfil')
        verbose_name_plural = _('Locais de Trabalho do Perfil')


class Endereco(CmjModelMixin):
    contato = models.ForeignKey(Contato,
                                verbose_name=('Contato'),
                                related_name='endereco_set',
                                on_delete=CASCADE)

    tipo = models.ForeignKey(
        TipoEndereco,
        related_name='endereco_set',
        blank=True, null=True, on_delete=SET_NULL,
        verbose_name=_('Tipo do Endereço'))

    trecho = models.ForeignKey(
        Trecho,
        verbose_name=_('Trecho'),
        related_name='endereco_set',
        blank=True, null=True, on_delete=SET_NULL)

    uf = models.CharField(max_length=2, blank=True, choices=UF,
                          verbose_name=_('Estado'))

    municipio = models.ForeignKey(
        Municipio,
        verbose_name=_('Município'),
        related_name='endereco_set',
        blank=True, null=True, on_delete=SET_NULL)

    cep = models.CharField(max_length=9, blank=True, default='',
                           verbose_name=_('CEP'))

    endereco = models.CharField(
        max_length=254, blank=True, default='',
        verbose_name=_('Endereço'),
        help_text=_('O campo endereço também é um campo de busca, nele '
                    'você pode digitar qualquer informação, inclusive '
                    'digitar o cep para localizar o endereço, e vice-versa!'))

    numero = models.CharField(max_length=50, blank=True, default='',
                              verbose_name=_('Número'))

    bairro = models.CharField(max_length=254, blank=True, default='',
                              verbose_name=_('Bairro'))
    distrito = models.ForeignKey(
        Distrito,
        verbose_name=Distrito._meta.verbose_name,
        related_name='endereco_set',
        blank=True, null=True, on_delete=SET_NULL)
    regiao_municipal = models.ForeignKey(
        RegiaoMunicipal,
        verbose_name=RegiaoMunicipal._meta.verbose_name,
        related_name='endereco_set',
        blank=True, null=True, on_delete=SET_NULL)

    complemento = models.CharField(max_length=30, blank=True, default='',
                                   verbose_name=_('Complemento'))

    class Meta:
        verbose_name = _('Endereço')
        verbose_name_plural = _('Endereços')

    def __str__(self):
        numero = (' - ' + self.numero) if self.numero else ''
        return self.endereco + numero


class EnderecoPerfil(Endereco):

    class Meta:
        proxy = True
        verbose_name = _('Endereço do Perfil')
        verbose_name_plural = _('Endereços do Perfil')


class FiliacaoPartidaria(models.Model):
    contato = models.ForeignKey(Contato,
                                verbose_name=('Contato'),
                                related_name='filiacaopartidaria_set',
                                on_delete=CASCADE)

    data = models.DateField(verbose_name=_('Data de Filiação'))
    partido = models.ForeignKey(Partido,
                                related_name='filiacaopartidaria_set',
                                verbose_name=Partido._meta.verbose_name)
    data_desfiliacao = models.DateField(
        blank=True, null=True, verbose_name=_('Data de Desfiliação'))

    @property
    def contato_nome(self):
        return str(self.contato)

    class Meta:
        verbose_name = _('Filiação Partidária')
        verbose_name_plural = _('Filiações Partidárias')

    def __str__(self):
        return str(self.partido)