# -*- coding: utf-8 -*-
"""
CursosXYZ
Project for Software Development III class, and my first Django tryout. 

@copyright: 2010 Matias Schertel <mschertel@gmail.com>
@license: GNU General Public License.
"""
"""
http://www.aprendendodjango.com/o-rss-e-o-entregador-fiel/
"""
from django.contrib.syndication.feeds import Feed
from models import Turma

# FEED: proximas_turmas
class ProximasTurmas(Feed):
    title = 'Próximas Turmas - Cursos XYZ'
    link = '/'

    def items(self):
        return [t for t in Turma.objects.filter(ativa=True).order_by('data_inicio') if t.is_aberta()]

    def item_link(self, turma):
        return turma.get_absolute_url()
