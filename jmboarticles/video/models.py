from django.db import models
from jmboarticles.managers import PublishedManager

# Create your models here.
class Video(models.Model):
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=True)
    publish_on = models.DateTimeField(blank=True, null=True)

    # content
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    video = models.FileField(upload_to='content/video')
    thumbnail = models.ImageField(upload_to='content/thumbnails')

    # Meta
    author = models.ForeignKey('auth.User', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    last_view_date = models.DateTimeField(blank=True, null=True)
    like_count = models.PositiveIntegerField(default=0)
    like_users = models.ManyToManyField('auth.User', related_name='liked_videos', blank=True)

    # Social
    comments_enabled = models.BooleanField(default=True)

    # Sites
    sites = models.ManyToManyField('sites.Site')

    objects = models.Manager()
    published_objects = PublishedManager()

    def __unicode__(self):
        return self.title