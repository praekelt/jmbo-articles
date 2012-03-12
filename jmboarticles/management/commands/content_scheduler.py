from django.core.management.base import BaseCommand
from jmboarticles.models import Article
from jmboarticles.poll.models import Poll
from jmboarticles.featured.models import Item
from datetime import datetime

class Command(BaseCommand):
    help = 'Publish content based on the publish_on fields'

    def handle(self, **options):
        classes = [Article, Poll, Item]
        for klass in classes:
            candidates = klass.objects.filter(
                            publish_on__lt=datetime.now(),
                            published=False)
            if candidates.exists():
                candidates.update(published=True