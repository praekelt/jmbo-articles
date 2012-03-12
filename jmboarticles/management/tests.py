from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.contrib.sites.models import Site
from jmboarticles.management.commands import content_scheduler
from jmboarticles.models import Article
from datetime import datetime, timedelta


class ContentSchedulerTestCase(TestCase):

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

    def test_content_scheduler(self):
        yesterday = datetime.now() - timedelta(days=1)
        tomorrow = datetime.now() + timedelta(days=1)

        article1 = self.mk_article(published_on=None, published=False,
                                    publish_on=yesterday)
        article2 = self.mk_article(published_on=None, published=False,
                                    publish_on=tomorrow)
        cs = content_scheduler.Command()
        cs.handle()
        [article1, article2] = Article.objects.filter(
                                pk__in=[article1.pk, article2.pk])
        self.assertTrue(article1.published)
        self.assertTrue(article1.published_on)
        self.assertFalse(article2.published)
