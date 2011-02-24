# -*- coding: utf-8 -*-
"""
CursosXYZ
Project for Software Development III class, and my first Django tryout. 

@copyright: 2010 Matias Schertel <mschertel@gmail.com>
@license: GNU General Public License.
"""
"""
http://docs.djangoproject.com/en/dev/intro/tutorial01/
Modelos
http://docs.djangoproject.com/en/dev/topics/forms/modelforms/
http://docs.djangoproject.com/en/dev/ref/models/fields/
Validators
http://docs.djangoproject.com/en/dev/ref/validators/
http://docs.djangoproject.com/en/dev/ref/models/instances/#validating-objects
Queries
http://docs.djangoproject.com/en/dev/topics/db/queries/
Admin
http://docs.djangoproject.com/en/dev/ref/contrib/admin/
"""
from django.db import models
from datetime import date
from django.db.models import signals
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse

# Model Categoria
class Categoria(models.Model):
    nome = models.CharField(max_length=75, unique=True)
    slug = models.SlugField(max_length=75, blank=True)
    ativa = models.BooleanField("Ativa")
    descricao = models.TextField('Descrição', max_length=200, help_text='Breve descrição da categoria.')
    
    class Meta:
        ordering = ('nome',)
        verbose_name_plural = "categorias"
    
    def get_absolute_url(self):
        return reverse('CursosXYZ.cursos.views.categoria', kwargs={'slug': self.slug})
    
    def qnt_cursos_total(self):
        return self.curso_set.count()
    qnt_cursos_total.short_description = 'Cursos Totais'
    
    def qnt_cursos_ativos(self):
        return len([c for c in self.curso_set.all() if c.ativa])
    qnt_cursos_ativos.short_description = 'Cursos Ativos'
        
    def __unicode__(self):
        return self.nome

# Model Professor
class Professor(models.Model):
    nome = models.CharField(max_length=200)
    slug = models.SlugField(max_length=75, blank=True)
    email = models.EmailField(unique=True)
    curriculo = models.TextField('Currículo', max_length=500, help_text='Resumo da experiência do professor.')
    # TODO: Colocar campo foto?
    
    class Meta:
        ordering = ('nome',)
        verbose_name_plural = "professores"
    
    def get_absolute_url(self):
        return reverse('CursosXYZ.cursos.views.professor', kwargs={'slug': self.slug})
    
    def qnt_turmas_total(self):
        return self.turma_set.count()
    qnt_turmas_total.short_description = 'Turmas Totais'
    
    def qnt_turmas_abertas(self):
        return len([t for t in self.turma_set.all() if t.is_aberta()])
    qnt_turmas_abertas.short_description = 'Turmas Abertas'
    
    def __unicode__(self):
        return self.nome

# Model Curso
class Curso(models.Model):
    nome = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=75, blank=True)
    ativa = models.BooleanField("Ativo")
    pre_requisitos = models.TextField('Pré-requisitos', max_length=500, blank=True, help_text='Conhecimentos necessários para o bom entendimento do conteúdo.')
    publico_alvo = models.TextField('Público Alvo', max_length=500, blank=True, help_text='Público alvo.')
    descricao = models.TextField('Descrição', max_length=1000, help_text='Descrição dos conteúdos abordados.')
    observacoes = models.TextField('Observações', max_length=500, blank=True, help_text='Informações adicionais.')
    categorias = models.ManyToManyField(Categoria)
    
    class Meta:
        verbose_name_plural = "cursos"
        ordering = ('nome',)
    
    def get_absolute_url(self):
        return reverse('CursosXYZ.cursos.views.curso', kwargs={'slug': self.slug})
    
    def qnt_turmas_total(self):
        return self.turma_set.count()
    qnt_turmas_total.short_description = 'Total'
    
    def qnt_turmas_ativas(self):
        return self.turma_set.filter(ativa=True).count()
    qnt_turmas_ativas.short_description = 'Ativas'
    
    def qnt_turmas_inativas(self):
        return self.turma_set.filter(ativa=False).count()
    qnt_turmas_inativas.short_description = 'Inativas'
    
    def qnt_turmas_abertas(self):
        return len([t for t in self.turma_set.all() if t.is_aberta()])
    qnt_turmas_abertas.short_description = 'Abertas'
    
    def __unicode__(self):
        return self.nome

# Model Turma
class Turma(models.Model):
    curso = models.ForeignKey(Curso)
    ativa = models.BooleanField("Ativa")
    aos_sabados = models.BooleanField('Sábados')
    data_inicio = models.DateField('Início', help_text='Data de Início, se for aos sábados, deve ser um sábado.',)
    data_fim = models.DateField('Fim', help_text='Data de Término, se for aos sábados, deve ser um sábado.')
    horario_inicio = models.TimeField('Início', help_text='Horário de Início.')
    horario_fim = models.TimeField('Fim', help_text='Horário de Término.')
    local = models.CharField(max_length=150, help_text='Local de realização das aulas.')
    professores = models.ManyToManyField(Professor)
    observacoes = models.CharField('Observações', max_length=300, blank=True, help_text='Informações adicionais.')
    
    class Meta:
        verbose_name_plural = "turmas"
        # ordering = ('data_inicio',)
    
    def get_absolute_url(self):
        return reverse('CursosXYZ.cursos.views.turma', kwargs={'slug': self.curso.slug, 'turma_id': self.id})
    
    def lista_professores(self):
        return ', '.join([e.nome for e in self.professores.all()])
    lista_professores.short_description = 'Professores'
    
    def is_aberta(self):
        '''
        Retorna True somente se a turma estiver ativa e a data de início for maior que a data atual e o curso a qual pertence estiver ativo
        '''
        return self.data_inicio > date.today() and self.ativa and self.curso.ativa
    is_aberta.short_description = 'Aberta'
    is_aberta.boolean = True
    
    def curso_codigo(self):
        return '{0} ({1})'.format(self.curso, self.codigo_turma())
    
    def codigo_turma(self):
        return '{0:0>4}'.format(self.id)
    
    def __unicode__(self):
        return '{0}'.format(self.id)
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.data_inicio > self.data_fim:
            raise ValidationError('Data Início não pode ser superior a Data Fim.')
        if self.horario_inicio > self.horario_fim:
            raise ValidationError('Horário Início não pode ser superior a Horário Fim.')
        if self.aos_sabados and self.data_inicio.isoweekday() is not 6:
            raise ValidationError('Um curso aos sábados deve iniciar em um sábado.')
        if self.aos_sabados and self.data_fim.isoweekday() is not 6:
            raise ValidationError('Um curso aos sábados deve terminar em um sábado.')
        if not self.aos_sabados and self.data_inicio.isoweekday() in (6,7):
            raise ValidationError('Um curso semanal deve iniciar em um dia útil.')
        if not self.aos_sabados and self.data_fim.isoweekday() in (6,7):
            raise ValidationError('Um curso semanal deve terminar em um dia útil.')

# Slugify
def pre_save_slugify(signal, instance, sender, **kwargs):
    """Este signal gera um slug automaticamente. Ele verifica se ja existe um
    artigo com o mesmo slug e acrescenta um numero ao final para evitar
    duplicidade"""
    classe = instance.__class__.__name__
    if not instance.slug:
        slug = slugify(instance.nome)
        novo_slug = slug
        contador = 0
        while eval(classe).objects.filter(slug=novo_slug).exclude(id=instance.id).count() > 0:
            contador += 1
            novo_slug = '%s-%d'%(slug, contador)
        instance.slug = novo_slug
signals.pre_save.connect(pre_save_slugify, sender=Categoria)
signals.pre_save.connect(pre_save_slugify, sender=Curso)
signals.pre_save.connect(pre_save_slugify, sender=Professor)
