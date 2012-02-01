from jmboarticles.video.models import Video
from django.template import Library


register = Library()

@register.simple_tag(takes_context=True)
def get_featured_videos(context, limit=5, var_name='video_list'):
    """
    Places a list of videos into the template context.

    Usage:
    {% get_videos `limit` `var_name` %}
    """

    context[var_name] = Video.published_objects.filter(featured=True)
    return ""
#register.assignment_tag(get_featured_articles)
