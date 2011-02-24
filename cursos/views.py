# -*- coding: utf-8 -*-
"""
CursosXYZ
Project for Software Development III class, and my first Django tryout. 

@copyright: 2010 Matias Schertel <mschertel@gmail.com>
@license: GNU General Public License.
"""
"""
http://docs.djangoproject.com/en/1.2/intro/tutorial03/
http://docs.djangoproject.com/en/1.2/
Templates
http://docs.djangoproject.com/en/dev/ref/templates/
"""
from django.shortcuts import render_to_response
from django.http import Http404
from CursosXYZ.cursos.models import Curso, Turma, Professor, Categoria

def listas_layout():
    proximas_turmas = [t for t in Turma.objects.filter(ativa=True).order_by('data_inicio')[5:] if t.is_aberta()]
    lista_categorias = Categoria.objects.filter(ativa=True)
    return {'proximas_turmas': proximas_turmas, 'lista_categorias': lista_categorias}

# Index
def index(request):
    vars = {}
    vars.update(listas_layout())
    return render_to_response('cursos/index.html', vars)


# Lista de Cursos
def cursos(request):
    cursos = Curso.objects.filter(ativa=True)
    vars = {'cursos': cursos}
    vars.update(listas_layout())
    return render_to_response('cursos/cursos.html', vars)

# Detalhes Curso
def curso(request, slug):
    try:
        curso = Curso.objects.get(slug=slug)
        categorias = curso.categorias.filter(ativa=True)
        turmas = [t for t in curso.turma_set.filter(ativa=True).order_by('data_inicio') if t.is_aberta()]
    except Curso.DoesNotExist:
        raise Http404
    vars = {'curso': curso, 'categorias': categorias, 'turmas': turmas}
    vars.update(listas_layout())
    return render_to_response('cursos/curso.html', vars)

# Detalhes Turma do Curso
def turma(request, slug, turma_id):
    try:
        curso = Curso.objects.get(slug=slug)
        turma = curso.turma_set.get(pk=turma_id)
        professores = turma.professores.all()
    except Curso.DoesNotExist:
        raise Http404
    except turma.DoesNotExist:
        raise Http404
    vars = {'curso': curso, 'turma': turma, 'professores': professores}
    vars.update(listas_layout())
    return render_to_response('cursos/turma.html', vars)

# Detalhes Turma do Curso (popup)
def turma_popup(request, slug, turma_id):
    try:
        curso = Curso.objects.get(slug=slug)
        turma = curso.turma_set.get(pk=turma_id)
        professores = turma.professores.all()
    except Curso.DoesNotExist:
        raise Http404
    except turma.DoesNotExist:
        raise Http404
    return render_to_response('cursos/turma_popup.html', {'curso': curso, 'turma': turma, 'professores': professores})

# Lista Professores
def professores(request):
    professores = Professor.objects.all()
    vars = {'professores': professores}
    vars.update(listas_layout())
    return render_to_response('cursos/professores.html', vars)

# Detalhes Professor
def professor(request, slug):
    try:
        professor = Professor.objects.get(slug=slug)
    except Curso.DoesNotExist:
        raise Http404
    vars = {'professor': professor}
    vars.update(listas_layout())
    return render_to_response('cursos/professor.html', vars)

# Detalhes Professor (popup)
def professor_popup(request, slug):
    try:
        professor = Professor.objects.get(slug=slug)
    except Curso.DoesNotExist:
        raise Http404
    return render_to_response('cursos/professor_popup.html', {'professor': professor})

# TODO: Lista de Categorias
def categorias(request):
    categorias = Categoria.objects.filter(ativa=True)
    vars = {'categorias': categorias}
    vars.update(listas_layout())
    return render_to_response('cursos/categorias.html', vars)

# TODO: Detalhes Categoria
def categoria(request, slug):
    try:
        categoria = Categoria.objects.get(slug=slug)
        cursos = Curso.objects.filter(categorias=categoria, ativa=True)
    except Curso.DoesNotExist:
        raise Http404
    vars = {'categoria': categoria, 'cursos': cursos}
    vars.update(listas_layout())
    return render_to_response('cursos/categoria.html', vars)
