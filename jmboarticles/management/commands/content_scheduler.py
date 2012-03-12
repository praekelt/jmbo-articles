from django.core.management.base import BaseCommand
from jmboarticles.models import Article
from jmboarticles.poll.models import Poll
from jmboarticles.featured.models import Item
from datetime import datetime

class Command(BaseCommand):
    help = 'Publish content based on the publish_on fields'

    def handle(self, **options):
        # Do articles
        articles = Article.objects.filter(
                        publish_on__lt=datetime.now(),
                        publish_on__isnull=False,
                        published=False)
        articles.update(published=True,
                                published_on=datetime.now())

        # Do polls
        polls = Poll.objects.filter(
                    publish_on__lt=datetime.now(),
                    published=False)
        polls.update(published=True)

        # Do items
        items = Item.objects.filter(
                    publish_on__lt=datetime.now(),
                    published=False)
        items.update(published=True)
