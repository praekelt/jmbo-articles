from datetime import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from poll.models import Poll, Choice


class PollTestCase(TestCase):

    def setUp(self):
        # user
        self.user = User.objects.create_user('test', 'test@domain.com', 'test')
        self.user.is_active = True
        self.user.save()
        # poll
        self.poll = Poll.objects.create(question='Colour?')
        self.poll.sites.add(Site.objects.get_current())

        self.choice_1 = self.poll.choice_set.create(choice='Red')
        self.choice_2 = self.poll.choice_set.create(choice='Green')
        self.choice_3 = self.poll.choice_set.create(choice='Blue')

    def tearDown(self):
        pass

    def test_has_user_voted(self):
        self.assertFalse(self.poll.has_user_voted(self.user))
        # vote!
        self.poll.vote(self.user, self.choice_1.pk)
        self.assertTrue(self.poll.has_user_voted(self.user))

    def test_published_manager_published(self):
        # published
        self.poll.published = True
        self.poll.save()
        self.assertEquals(len(Poll.published_objects.all()), 1)
        # unpublished
        self.poll.published = False
        self.poll.save()
        self.assertEquals(len(Poll.published_objects.all()), 0)

    def test_poll_vote_view(self):

        self.assertEqual(self.choice_2.vote_count, 0)
        self.client.login(username='test', password='test')
        resp = self.client.post(reverse('poll_vote', args=[self.poll.pk]), {
            'choice_pk': self.choice_1.pk,
        })

        choice = Choice.objects.get(pk=self.choice_1.pk)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(choice.vote_count, 1)
        self.assertTrue(self.poll.has_user_voted(self.user))
