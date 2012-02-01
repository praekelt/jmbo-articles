from datetime import datetime
from django import template

register = template.Library()

from poll.models import Poll, Choice



@register.inclusion_tag('poll/tag_poll.html', takes_context=True)
def show_poll(context, poll):
    return {'poll': poll, 'user': context['user']}


@register.simple_tag(takes_context=True)
def get_featured_poll(context, var_name='featured_poll'):
    try:
        context[var_name] = Poll.published_objects.filter(featured=True).latest('publish_on')
    except Poll.DoesNotExist:
        context[var_name] = None
    return ""

@register.filter
def is_published(poll):
    if poll.published and poll.publish_on <= datetime.now():
        return True
    return False

@register.filter
def has_user_voted(poll, user):
    return poll.has_user_voted(user)


@register.simple_tag(takes_context=True)
def get_poll_results(context, poll, var_name='poll_result_list'):
    """
    The poll's results are typically displayed to a user when they've voted on
    a poll.

    This tag is used to calculate a total as well as a percentage of votes
    received per choice.


    """
    choice_list = poll.choice_set.all()
    total_votes = sum(c.vote_count for c in choice_list)
    for c in choice_list:
        if total_votes > 0:
            c.percentage = '%.0f' % round((float(c.vote_count) / float(total_votes)) * 100)
        else:
            c.percentage = "0"

    context[var_name] = choice_list

    return ""
