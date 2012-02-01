from datetime import datetime

from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from jmboarticles.poll.managers import PublishedManager


class Poll(models.Model):
    featured = models.BooleanField(default=False,
        help_text="Featured polls appear on the homepage.")
    published = models.BooleanField(default=True)
    publish_on = models.DateTimeField(null=True, blank=True)
    question = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='poll/', blank=True)
    participants = models.ManyToManyField(User, editable=False)
    sites = models.ManyToManyField(Site)

    objects = models.Manager()
    published_objects = PublishedManager()

    class Meta:
        ordering = ('-id',)
        get_latest_by = 'id'

    def __unicode__(self):
        return self.question

    @permalink
    def get_absolute_url(self):
        return ('poll_detail', None, {
            'pk': self.pk
        })

    def has_user_voted(self, user):
        if user.is_authenticated():
            return self.participants.filter(pk=user.pk).exists()

    def vote(self, user, choice_pk):
        if not self.has_user_voted(user):
            choice = self.choice_set.get(pk=choice_pk)
            choice.vote_count += 1
            choice.vote_users.add(user)
            choice.save()
            self.participants.add(user)
            self.save()


class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    vote_count = models.PositiveIntegerField(default=0)
    vote_users = models.ManyToManyField(User, editable=False)

    class Meta:
        ordering = ('order',)

    def __unicode__(self):
        return self.choice
