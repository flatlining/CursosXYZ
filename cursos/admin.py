# -*- coding: utf-8 -*-
"""
CursosXYZ
Project for Software Development III class, and my first Django tryout. 

@copyright: 2010 Matias Schertel <mschertel@gmail.com>
@license: GNU General Public License.
"""
"""
Admin
http://docs.djangoproject.com/en/dev/intro/tutorial02/
http://docs.djangoproject.com/en/dev/ref/contrib/admin/
Actions
http://docs.djangoproject.com/en/dev/ref/contrib/admin/actions/
"""
from CursosXYZ.cursos.models import Turma, Curso, Categoria, Professor
from django.contrib import admin

# Ações
def acao_ativar(self, request, queryset):
    quantidade = queryset.update(ativa=True)
    if quantidade == 1:
        message_bit = '1 item foi ativado'
    else:
        message_bit = '{0} itens foram ativados'.format(quantidade)
    self.message_user(request, '{0} com sucesso.'.format(message_bit))
acao_ativar.short_description = "Ativar Selecionados"

def acao_desativar(self, request, queryset):
    quantidade = queryset.update(ativa=False)
    if quantidade == 1:
        message_bit = '1 item foi desativado'
    else:
        message_bit = '{0} itens foram desativados'.format(quantidade)
    self.message_user(request, '{0} com sucesso.'.format(message_bit))
acao_desativar.short_description = "Desativar Selecionados"

# Curso Admin
class TurmaInline(admin.TabularInline):
    model = Turma
    extra = 2

class CursoAdmin(admin.ModelAdmin):
    list_display = ('ativa', 'nome', 'qnt_turmas_ativas', 'qnt_turmas_abertas', 'qnt_turmas_inativas', 'qnt_turmas_total')
    actions = [acao_ativar, acao_desativar]
    list_display_links = ['nome']
    readonly_fields = ('slug',)
    list_filter = ('ativa', 'categorias')
    fieldsets = [
        ('Curso',       {'fields': ['ativa', 'nome']}),
        ('Informações', {'fields': ['pre_requisitos', 'publico_alvo', 'descricao']}),
        ('Observações',          {'fields': ['observacoes'], 'classes': ['collapse']}),
        (None,          {'fields': ['categorias']}),
        ('Slug',        {'fields': ['slug'], 'classes': ['collapse']}),
    ]
    inlines = [TurmaInline]

admin.site.register(Curso, CursoAdmin)

# Categoria Admin
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('ativa', 'nome', 'qnt_cursos_ativos','qnt_cursos_total')
    actions = [acao_ativar, acao_desativar]
    readonly_fields = ('slug',)
    list_display_links = ['nome']
    fieldsets = [
        (None,       {'fields': ['ativa', 'nome', 'descricao']}),
        ('Slug',     {'fields': ['slug'], 'classes': ['collapse']}),
    ]

admin.site.register(Categoria, CategoriaAdmin)

# Turma Admin
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('ativa', 'is_aberta', 'curso_codigo' , 'data_inicio', 'data_fim', 'aos_sabados', 'horario_inicio', 'horario_fim', 'lista_professores')
    list_display_links = ['curso_codigo']
    actions = [acao_ativar, acao_desativar]
    list_filter = ['ativa', 'curso', 'aos_sabados']
    date_hierarchy = 'data_inicio'
    fieldsets = [
        ('Turma',       {'fields': ['ativa', 'curso']}),
        ('Informações', {'fields': ['data_inicio', 'data_fim', 'aos_sabados', 'horario_inicio', 'horario_fim', 'local']}),
        ('Observações', {'fields': ['observacoes'], 'classes': ['collapse']}),
        ('Professores', {'fields': ['professores']}),
    ]

admin.site.register(Turma, TurmaAdmin)

# Professor Admin
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'qnt_turmas_abertas', 'qnt_turmas_total')
    search_fields = ['nome']
    list_editable = ('email',)
    readonly_fields = ('slug',)
    fieldsets = [
        (None,       {'fields': ['nome', 'email', 'curriculo']}),
        ('Slug',     {'fields': ['slug'], 'classes': ['collapse']}),
    ]

admin.site.register(Professor, ProfessorAdmin)
