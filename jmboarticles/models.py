from datetime import datetime

from dirtyfields import DirtyFieldsMixin

from django.db import models
from django.db.models import permalink
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.comments.moderation import moderator
from django.contrib.contenttypes.models import ContentType

from jmboarticles.poll.models import Poll
from jmboarticles.video.models import Video
from jmboarticles.managers import PublishedManager
from jmbocomments.models import YALCommentModerator


class Article(models.Model, DirtyFieldsMixin):
    published = models.BooleanField(default=True)
    published_on = models.DateTimeField(blank=True, null=True)
    publish_on = models.DateTimeField(blank=True, null=True)
    on_homepage = models.BooleanField('Always display on the homepage?', default=False)

    # Content
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='article/', blank=True)
    content = models.TextField()
    source_name = models.CharField(max_length=255, blank=True, null=True)
    source_link = models.URLField(verify_exists=False, blank=True, null=True)

    # Organisation
    categories = models.ManyToManyField('category.Category', blank=True, null=True)
    tags = models.ManyToManyField('category.Tag', blank=True, null=True)

    # Extra Content
    poll = models.ForeignKey(Poll, blank=True, null=True)
    video = models.ForeignKey(Video, blank=True, null=True)
    linked_article = models.ForeignKey('jmboarticles.Article', blank=True, null=True)
    linked_page = models.ForeignKey('flatpages.FlatPage', blank=True, null=True)

    # Meta
    author = models.ForeignKey(User, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    view_count = models.PositiveIntegerField(default=0)
    last_view_date = models.DateTimeField(blank=True, null=True)
    like_count = models.PositiveIntegerField(default=0)
    like_users = models.ManyToManyField(User, related_name='liked_articles')

    # Social
    comments_enabled = models.BooleanField(default=True)

    # Sites
    sites = models.ManyToManyField(Site)

    objects = models.Manager()
    published_objects = PublishedManager()

    class Meta:
        ordering = ('-published_on',)
        get_latest_by = ('published_on',)

    def inc_view_count(self):
        self.view_count += 1
        self.last_view_date = datetime.now()
        self.save()

    def __unicode__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return ('article_detail', None, {
            'pk': self.pk
        })

def update_published_on_field(sender, **kwargs):
    instance = kwargs.get('instance')
    if 'published' in instance.get_dirty_fields():
        if instance.published:
            instance.published_on = datetime.now()
        else:
            instance.published_on = datetime.min
    elif instance.published and not instance.published_on:
        instance.published_on = instance.updated

pre_save.connect(update_published_on_field, sender=Article)

class ArticleCommentModerator(YALCommentModerator):
    email_notification = False
    enable_field = 'comments_enabled'

    def allow(self, comment, content_object, request):
        content_type = ContentType.objects.get_for_model(Article)
        return self.check_for_duplicate_comment_submission(
                comment, content_type, content_object.pk, request.user)

# FIXME: bug in Django, tries to load it twice.
#        https://code.djangoproject.com/ticket/11917
if Article not in moderator._registry:
    moderator.register(Article, ArticleCommentModerator)

