from datetime import datetime
from django.template import Library

register = Library()


from jmboarticles.featured.models import Item

# this would work very well as an assignment tag; but it's a Django development 
# version feature. So I'm haxing it for now.

@register.simple_tag(takes_context=True)
def get_featured_items(context, limit=5, var_name='featured_item_list'):
    """
    Places a list of featured items into the template context.
      
    Usage:
    {% get_featured_items `limit` `var_name` %}

    """
    
    context[var_name] = Item.published_objects.all()[:limit]
    return ""
#register.assignment_tag(get_featured_articles)