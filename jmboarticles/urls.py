from django.conf.urls.defaults import patterns, include, url
from django.views.generic.list import ListView

from jmboarticles.models import Article

urlpatterns = patterns('jmboarticles.views',
    url(r'^(?P<pk>\d+)/$', 'article_detail', name='article_detail'),
    url(r'^(?P<pk>\d+)/p/(?P<page>\d+)/$', 'article_detail', name='article_detail'),
    url(r'^(?P<pk>\d+)/like/$', 'article_like', name='article_like'),

    url(r'^$', 'article_list', name='article_list'),
    url(r'^p/(?P<page>\d+)/$', 'article_list', name='article_list'),
)
