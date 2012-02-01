from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import reverse

from jmboarticles.poll.models import Poll


def poll_detail(request, pk, show_results=False):
    poll = get_object_or_404(
        Poll.objects.all().select_related('choices'), pk=pk)
    return direct_to_template(request, 'poll/poll_detail.html', {
        'poll': poll, 'show_results': show_results
    })


def vote(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    choice_pk = request.POST.get('choice_pk', None)
    if choice_pk:
        poll.vote(request.user, choice_pk)
    return HttpResponseRedirect(reverse('poll_detail', kwargs={'pk': poll.pk}))


def poll_detail_results(request, pk):
    return poll_detail(request, pk, True)
