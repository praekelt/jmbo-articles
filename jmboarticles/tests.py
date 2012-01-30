from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.contrib.sites.models import Site
from jmboarticles.models import Article
from datetime import datetime


class ArticleTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def tearDown(self):
        pass

    def mk_article(self, **kwargs):
        defaults = {
            'title': 'title',
            'content': 'content',
            'published': True,
            'published_on': datetime.now(),
        }
        defaults.update(kwargs)
        defaults.update({
            'slug': slugify(defaults['title']),
        })
        article = Article(**defaults)
        article.save()
        article.sites.add(Site.objects.get_current())
        return article

    def test_on_homepage_boolean(self):
        """
        if the `on_homepage` boolean is set
        it should always be displayed on the
        homepage regardless if there are more
        recent articles.
        """
        oldest_article = self.mk_article(title='on homepage article',
                                            on_homepage=True)
        for i in range(0,10):
            article = self.mk_article(title='article-%s' % i)
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'on homepage article')
        self.assertNotContains(response, 'article-0')
