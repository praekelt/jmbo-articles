from datetime import datetime

from django.conf import settings
from django.db.models import Manager


class PublishedManager(Manager):
    def get_query_set(self):
        return super(PublishedManager, self).get_query_set().filter(
        	published=True,
        	sites__id__exact=settings.SITE_ID
        )