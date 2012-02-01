from datetime import datetime
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.sites.models import Site
from managers import PublishedManager


class Item(models.Model):
    published = models.BooleanField(default=True)
    publish_on = models.DateTimeField(blank=True, null=True)
    title = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    link = models.CharField(max_length=255)
    image = models.ImageField(upload_to='featured/', blank=True)
    sites = models.ManyToManyField(Site)

    objects = models.Manager()
    published_objects = PublishedManager()

    class Meta:
        pass

    def __unicode__(self):
        return self.title