# -*- coding: utf-8 -*-
"""
CursosXYZ
Project for Software Development III class, and my first Django tryout. 

@copyright: 2010 Matias Schertel <mschertel@gmail.com>
@license: GNU General Public License.
"""
"""
URLs
http://docs.djangoproject.com/en/dev/howto/static-files/
http://docs.djangoproject.com/en/dev/topics/http/urls/
Templates
http://www.djangobook.com/en/beta/chapter04/
http://docs.djangoproject.com/en/dev/ref/templates/
"""
from django.conf.urls.defaults import patterns, include

from django.contrib import admin
from settings import MEDIA_ROOT
admin.autodiscover()

from cursos.feeds import ProximasTurmas

urlpatterns = patterns('',
    # Example:
    # (r'^CursosXYZ/', include('CursosXYZ.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

# Public Views
urlpatterns += patterns('CursosXYZ.cursos.views',
    (r'^$', 'index'),
    
    (r'^cursos/$', 'cursos'),
    (r'^cursos/(?P<slug>[\w_-]+)/$', 'curso'),
    
    (r'^cursos/(?P<slug>[\w_-]+)/(?P<turma_id>\d+)/$', 'turma'),
    (r'^cursos/(?P<slug>[\w_-]+)/(?P<turma_id>\d+)/popup/$', 'turma_popup'),
    
    (r'^professores/$', 'professores'),
    (r'^professores/(?P<slug>[\w_-]+)/$', 'professor'),
    (r'^professores/(?P<slug>[\w_-]+)/popup/$', 'professor_popup'),
    
    (r'^categorias/$', 'categorias'),
    (r'^categorias/(?P<slug>[\w_-]+)/$', 'categoria'),
)

# Static Files
urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT, 'show_indexes': True}),
)

# RSS Feed
urlpatterns += patterns('',
    (r'^rss/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': {'proximas_turmas': ProximasTurmas}}),
)
