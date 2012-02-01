from django.conf.urls.defaults import *

urlpatterns = patterns('jmboarticles.poll.views',
    url(r'^(?P<pk>\d+)/$', 'poll_detail', name='poll_detail'),
    url(r'^(?P<pk>\d+)/vote/$', 'vote', name='poll_vote'),
    url(r'^(?P<pk>\d+)/results/$', 'poll_detail_results', name='poll_results'),
)
