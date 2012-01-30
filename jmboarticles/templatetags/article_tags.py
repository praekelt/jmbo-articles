from django.template import Library

register = Library()


from jmboarticles.models import Article

# this would work very well as an assignment tag; but it's a Django development
# version feature. So I'm haxing it for now.

@register.simple_tag(takes_context=True)
def get_articles(context, limit=5, var_name='article_list'):
    """
    Places a list of articles into the template context.

    Usage:
    {% get_articles `limit` `var_name` %}
    """

    fetch_columns = ['pk', 'image', 'title', 'description',
                        'updated', 'created', 'published_on']
    articles = Article.published_objects.all()
    # get the most recent articles to be published on the homepage
    # that don't have the `on_homepage` boolean set.
    recent_articles = articles.filter(on_homepage=False) \
                        .values(*fetch_columns)[:limit]

    # get the articles that always need to be displayed on the homepage
    # regardless of the created date
    homepage_articles = articles.filter(on_homepage=True) \
                        .values(*fetch_columns)
    display_articles = list(recent_articles) + list(homepage_articles)

    # sort them according to descending updated date
    context[var_name] = sorted(display_articles,
                            key=lambda article: article['published_on'],
                            reverse=True)
    return ""
