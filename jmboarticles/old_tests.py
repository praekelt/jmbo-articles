# from django.test import TestCase
# from django.test.client import Client
# from django.core.urlresolvers import reverse
# from django.conf import settings
# from django.contrib.auth.models import User
# from yal.models import sanitize_html, Article, Usage_log, Comment, \
#                         CommentLimitSettings, Banned_user, Banned_word, \
#                         STATUS_REPORTED, STATUS_APPROVED, STATUS_ABUSIVE, \
#                         Page, Template, ArticleOrderManager, LinkManager, \
#                         Video, LikeIt, CommentVote, CommentInactiveTimeSettings, \
#                         YourStoryCompetition, YourStoryEntry, Banner, \
#                         get_or_create_old_user
# from yal.models import User as OldUser
# from yal.competition.models import Quiz, Question, Answer, Competition
# from yal.widgets import AdminImageWidget, VodafoneLiveEditorWidget
# from category.models import Tag, Category

# from yal.admin import VideoAdmin, ArticleAdmin

# import tempfile
# import os.path
# from datetime import datetime, timedelta, time

# def reload_record(record):
#     return record.__class__.objects.get(pk=record.pk)

# def create_temp_file(data):
#     # make sure the video has a file linked to it
#     tmp_dir = os.path.join(settings.MEDIA_ROOT)
#     tmp_file = tempfile.NamedTemporaryFile(dir=tmp_dir)
#     tmp_file.write(data)
#     tmp_file.flush()
#     return tmp_file
# # 
# # class ReportAbuseTestCase(TestCase):
# #     
# #     def setUp(self):
# #         self.user = User.objects.create(username='27761234567')
# #         self.profile = self.user.get_profile()
# #         self.profile.msisdn = self.user.username
# #         self.profile.alias='test user'
# #         self.article = Article.objects.create(
# #                             title='test title',
# #                             content='<p>this is the content</p>',
# #                             state='published'
# #                         )
# #         self.comment = Comment.objects.create(
# #                         user = get_or_create_old_user('27761234567'),
# #                         new_user=self.user, 
# #                         article=self.article,
# #                         comment='this is the comment text'
# #                     )
# #     
# #     def tearDown(self):
# #         pass
# #     
# #     def test_approved_manager(self):
# #         self.assertEquals(Comment.approved.count(), 1)
# #         self.comment.status = STATUS_REPORTED
# #         self.comment.save()
# #         self.assertEquals(Comment.approved.count(), 0)
# #     
# #     def test_report_abuse_counter_and_flag(self):
# #         
# #         def report_abuse(comment, msisdn):
# #             client = Client()
# #             return client.get(
# #                 reverse('report_abuse', 
# #                     kwargs={
# #                         'markup': 'pml', 
# #                         'comment_id': comment.pk
# #                     }
# #                 ), {
# #                     'article': comment.article.pk
# #                 }, HTTP_X_UP_CALLING_LINE_ID=msisdn
# #             )
# #         
# #         self.assertEquals(self.comment.abuse_report_count, 0)
# #         
# #         # first time status shouldn't change but the counter should
# #         # be incremented with one
# #         report_abuse(self.comment, '27761234567')
# #         comment = reload_record(self.comment)
# #         self.assertEquals(comment.abuse_report_count, 1)
# #         self.assertEquals(comment.status, STATUS_APPROVED)
# #         self.assertEquals(comment.new_abuse_reporters.count(), 1)
# #         
# #         # second time it should be flagged as STATUS_REPORTED
# #         report_abuse(self.comment, '27761234568')
# #         comment = reload_record(self.comment)
# #         self.assertEquals(comment.abuse_report_count, 2)
# #         self.assertEquals(comment.status, STATUS_REPORTED)
# #         self.assertEquals(comment.new_abuse_reporters.count(), 2)
# #         
# #         # third time it should automatically be flagged STATUS_ABUSIVE
# #         report_abuse(self.comment, '27761234569')
# #         comment = reload_record(self.comment)
# #         self.assertEquals(comment.abuse_report_count, 3)
# #         self.assertEquals(comment.status, STATUS_ABUSIVE)
# #         self.assertEquals(comment.new_abuse_reporters.count(), 3)
# #     
# #     def test_remove_comment(self):
# #         client = Client()
# #         # success
# #         response = client.get(reverse('remove_comment', kwargs={'comment_id': self.comment.pk}))
# #         self.assertContains(response, 'has been removed')
# #         # repetition
# #         response = client.get(reverse('remove_comment', kwargs={'comment_id': self.comment.pk}))
# #         self.assertContains(response, 'already deleted this comment')
# #     
# #     def test_ban_user(self):
# #         client = Client()
# #         response = client.get(reverse('ban_user', kwargs={'comment_id': self.comment.pk}))
# #         self.assertContains(response, 'has been banned from posting comments')
# #         response = client.get(reverse('ban_user', kwargs={'comment_id': self.comment.pk}))
# #         self.assertContains(response, 'already deleted')
# #     
# #     def test_ban_user_and_remove_comments(self):
# #         client = Client()
# #         response = client.get(reverse('ban_user_and_remove_comments', kwargs={'comment_id': self.comment.pk}))
# #         self.assertContains(response, 'banned from posting comments')
# #         response = client.get(reverse('ban_user_and_remove_comments', kwargs={'comment_id': self.comment.pk}))
# #         self.assertContains(response, 'already deleted')
# #     
# # 
# # 
# # def post_comment(article, user, comment, alias='anonymously'):
# #     comment_url = reverse('comment_post', kwargs={
# #         'markup': 'pml', 
# #         'article_id': article.pk
# #     })
# #     client = Client()
# #     return client.get(comment_url, {
# #         'content': comment,
# #         'post-as': alias,
# #     }, HTTP_X_UP_CALLING_LINE_ID=user.username)
# # 
# # class CommentingTestCase(TestCase):
# #     
# #     def setUp(self):
# #         self.user = User.objects.create(username='27761234567')
# #         self.profile = self.user.get_profile()
# #         self.profile.msisdn = self.user.username
# #         self.profile.alias = 'test user'
# #         self.article = Article.objects.create(
# #                             title='test title',
# #                             content='<p>this is the content</p>',
# #                             state='published'
# #                         )
# #         # FIXME: this is way to over-engineered
# #         comment_limit = CommentLimitSettings.objects.create(
# #             daily_limit=10,
# #             messages_over_before_warning=9,
# #             almost_reached_daily_limit_warning_message='',
# #             one_more_comment_allowed_message='',
# #             limit_reached_message_title='',
# #             limit_reached_message_body=''
# #         )
# #     
# #     def tearDown(self):
# #         pass
# #     
# #     def test_banned_user(self):
# #         """A banned user isn't allowed to place comments"""
# #         b = Banned_user.objects.create(user=self.user)
# #         response = post_comment(self.article, self.user, 'hello')
# #         self.assertTemplateUsed(response, "pml/comment/user_banned.xml")
# #     
# #     def test_banned_word(self):
# #         """A comment with banned words isn't allowed to be placed"""
# #         w = Banned_word.objects.create(word='bad')
# #         response = post_comment(self.article, self.user, 'you know I\'m bad')
# #         self.assertTemplateUsed(response, 'pml/comment/word_banned.xml')
# #     
# #     def test_article_comments_enabled(self):
# #         """Comments cannot be placed for articles with comments_enabled=False"""
# #         self.article.comments_enabled = False
# #         self.article.save()
# #         response = post_comment(self.article, self.user, 'hello')
# #         self.assertTemplateUsed(response, 'pml/comment/comment_closed.xml')
# #         
# #     def test_user_comment_limit(self):
# #         """A user isn't allowed to post unlimited comments"""
# #         for i in range(0,10):
# #             # use i to generate the comment as there's a duplicate comment
# #             # check
# #             response = post_comment(self.article, self.user, 'hello %s' % i)
# #             self.assertTemplateUsed(response, 'pml/comment/comment_post.xml')
# #         
# #         # this one should render a different template as the limit has been 
# #         # reached
# #         response = post_comment(self.article, self.user, 'hello 11')
# #         self.assertTemplateUsed(response, 'pml/comment/comment_limit.xml')
# #     
# #     def test_duplicate_comment_trap(self):
# #         """Duplicate comments submitted within 5 minutes of each other
# #         should not be saved"""
# #         response = post_comment(self.article, self.user, 'hello')
# #         response = post_comment(self.article, self.user, 'hello')
# #         self.assertEquals(self.article.comment_set.count(), 1)
# #         
# #         # change the timestamp, should allow for duplicate submission
# #         last_comment = self.article.comment_set.get(comment='hello')
# #         last_comment.date_time = datetime.now() - timedelta(minutes=6)
# #         last_comment.save()
# #         
# #         # try again
# #         response = post_comment(self.article, self.user, 'hello')
# #         self.assertEquals(self.article.comment_set.count(), 2)
# #         
# #     def test_comment_voting(self):
# #         """register 1 vote per user"""
# #         post_comment(self.article, self.user, 'hello')
# #         comment = Comment.objects.latest('pk')
# #         
# #         client = Client(HTTP_X_UP_CALLING_LINE_ID='27761234567')
# #         # vote a number of times
# #         for i in range(0,5):
# #             response = client.get(reverse('comment_vote', kwargs={
# #                 'markup': 'pml',
# #                 'vote': 'like',
# #                 'comment_id': comment.pk
# #             }))
# #             self.assertContains(response, 'Thank you')
# #         
# #         # reload comment
# #         comment = reload_record(comment)
# #         # make sure vote is registered
# #         self.assertTrue(CommentVote.objects.filter(new_user=self.user, comment=comment).exists())
# #         votes = CommentVote.objects.filter(new_user=self.user, comment=comment)
# #         self.assertEquals(votes.count(), 1)
# #         self.assertEquals(votes.latest('pk').direction, '+')
# #     
# #     def test_active_comment_form(self):
# #         # ensure that there's an hour time window for commenting
# #         # for this test
# #         CommentInactiveTimeSettings.objects.create(
# #             message_title='the title',
# #             message_body='the body',
# #             # after hours start at this time
# #             start_time=(datetime.now() + timedelta(hours=1)).time(),  
# #             # and end at this time
# #             end_time=(datetime.now() - timedelta(hours=1)).time()
# #         )
# #         
# #         client = Client(HTTP_X_UP_CALLING_LINE_ID='27761234567')
# #         response = client.get(reverse('comment', kwargs={
# #             'markup': 'pml',
# #             'article_id': self.article.pk
# #         }))
# #         # there should be a FORM as we're within the timelimits
# #         self.assertContains(response, '<FIELD')
# #     
# #     def test_inactive_comment_form(self):
# #         # always put this test in the inactive commenting time
# #         CommentInactiveTimeSettings.objects.create(
# #             message_title='the title',
# #             message_body='the body',
# #             # after hours start at this time
# #             start_time=(datetime.now() - timedelta(hours=1)).time(),  
# #             # and end at this time
# #             end_time=(datetime.now() + timedelta(hours=1)).time()
# #         )
# #         client = Client(HTTP_X_UP_CALLING_LINE_ID='27761234567')
# #         response = client.get(reverse('comment', kwargs={
# #             'markup':'pml',
# #             'article_id': self.article.pk
# #         }))
# #         # there should be a FORM as we're within the timelimits
# #         self.assertNotContains(response, '<FIELD')
# #     
# #     def test_comment_limit_warning(self):
# #         # limit to 1 for this test case
# #         limit = CommentLimitSettings.objects.latest('pk')
# #         limit.daily_limit = 2
# #         limit.almost_reached_daily_limit_warning_message = 'almost daily limit!'
# #         limit.one_more_comment_allowed_message = 'this is your last comment'
# #         limit.save()
# #         
# #         # ensure that there's an hour time window for commenting
# #         # for this test
# #         CommentInactiveTimeSettings.objects.create(
# #             message_title='the title',
# #             message_body='the body',
# #             # after hours start at this time
# #             start_time=(datetime.now() + timedelta(hours=1)).time(),  
# #             # and end at this time
# #             end_time=(datetime.now() - timedelta(hours=1)).time()
# #         )
# #         client = Client(HTTP_X_UP_CALLING_LINE_ID='27761234567')
# #         response = client.get(reverse('comment', kwargs={
# #             'markup':'pml',
# #             'article_id': self.article.pk
# #         }))
# #         # should be a warning about almost hitting the limit
# #         self.assertContains(response, limit.almost_reached_daily_limit_warning_message)
# #         # post a comment
# #         post_comment(self.article, self.user, 'hello')
# #         # now there should be a message informing of this being the last message
# #         response = client.get(reverse('comment', kwargs={
# #             'markup':'pml',
# #             'article_id': self.article.pk
# #         }))
# #         self.assertContains(response, limit.one_more_comment_allowed_message)
# #     

# class UserTestCase(TestCase):
    
#     def setUp(self):
#         pass
    
#     def tearDown(self):
#         pass
    
#     def test_timestamps(self):
        
#         user = User.objects.create(username='27764493806')
#         profile = user.get_profile()
        
#         self.failUnless(profile.created_at)
#         self.failUnless(profile.updated_at)
        
#         original_created_at = profile.created_at
#         original_updated_at = profile.updated_at
        
#         # update to change updated_at
#         profile.alias = 'smn'
#         profile.save()
        
#         self.assertEquals(original_created_at, profile.created_at)
#         self.assertNotEquals(original_updated_at, profile.updated_at)
    
#     def test_created_at_fix(self):
#         user = User.objects.create_user('27764493806', 'user@domain.com', '27764493806')
#         user.save()
        
#         new_log = Usage_log(date_time='2010-1-1 00:00:00', 
#             item='1', 
#             item_title='An Article', 
#             item_type = 'article', 
#             location = '', 
#             user = get_or_create_old_user(user.username),
#             new_user = user)
#         new_log.save()
        
#         profile = user.get_profile()
#         first_log_entry = profile.get_first_log_entry()
#         profile.created_at = first_log_entry.date_time
#         profile.save()
        
#         profile = reload_record(profile)
        
#         self.assertEquals(profile.created_at, datetime(2010,1,1,0,0,0))


# class TestHtmlCleaning(TestCase):
#     """Vodafone Live is very picky about the HTML being generated, test that."""
#     def setUp(self):
#         pass
    
#     def tearDown(self):
#         pass
    
#     def test_sanitize_html_none(self):
#         """sanitize_html should return anempty string when given None"""
#         self.assertEquals('', sanitize_html(None))
    
#     def test_sanitize_html_rich_test(self):
#         """sanitize_html should parse the HTML input and return
#         html output that is suitable for Vodafone Live"""
#         rich_text = """
#         <p>
#             <em>convert to i</em><br>
#             <strong>convert to b</strong><br>
#             <u>leave as u</u><br>
#             <b>leave as b</b><br>
#             <!-- should be removed -->
#             <p name="should be removed">but element kept</p><br>
#             <img>invalid element content should stay</img>
#             <br />
#         </p>
#         """.strip()
        
#         result = sanitize_html(rich_text)
#         # check element conversions
#         self.assertTrue('<i>convert to i</i><br />' in result)
#         self.assertTrue('<b>convert to b</b><br />' in result)
#         self.assertTrue('<u>leave as u</u><br />' in result)
#         self.assertTrue('<b>leave as b</b><br />' in result)
#         # comment and attributes should be removed
#         self.assertTrue('should be removed' not in result)
#         # invalid tags should be removed
#         self.assertTrue('img' not in result)
#         self.assertTrue('invalid element content should stay' in result)

# class TestPageRendering(TestCase):
#     """Test the behaviour we have before I continue refactoring"""
#     def setUp(self):
#         self.client = Client(HTTP_X_UP_CALLING_LINE_ID='27761234567',
#                                 HTTP_X_VODAFONE_AREA='Cape Town',
#                                 HTTP_USER_AGENT='DjangoTestClient')
#         # the homepage
#         page = Page()
#         page.template = Template.objects.create(path='/page/homepage.xml', title='Homepage')
#         page.title = 'The Homepage'
#         page.state = 'published'
#         page.description = 'Description'
#         page.save()
        
#         # FIXME:    this whole content holder setup is confusing from a tech 
#         #           and content perspective
#         self.content_holder = Page()
#         self.content_holder.title = 'Content Holder'
#         self.content_holder.state = 'published'
#         self.content_holder.description = 'Description'
#         self.content_holder.template = Template.objects.create(path='/page/content_list.xml', title='Content Holder')
#         self.content_holder.save()
        
#         # link content holder as a child of the homepage, otherwise the content
#         # holder's children won't be rendered on the homepage.
#         LinkManager.objects.create(parent_page=page, child_page=self.content_holder)
        
#         # create a 'featured' tag, featured == display on homepage
#         self.featured_tag, _ = Tag.objects.get_or_create(title='featured')
        
#         # video for download
#         self.video = Video(title='Video', description='Description')
#         self.video.save()
        
#         # article for viewing
#         self.article = Article.objects.create(title='test article', state='published')
#         self.article.articleordermanager_set.create(page=self.content_holder)
        
#         # key for video download
#         from yal.views import generate_key
#         key_params = ''.join([str(self.video.pk), 'DjangoTestClient'])
#         self.video_key = generate_key(key_params)
        
#         # create the quiz
#         self.competition = Competition.objects.create(title='competition')
#         self.quiz = Quiz.objects.create(title='quiz', competition=self.competition)
    
#     def tearDown(self):
#         pass
    
#     def test_render_homepage(self):
#         """it should render, obviously"""
        
#         # create 5 random articles
#         for i in range(0,5):
#             article = Article.objects.create(title='test article %s' % i,
#                                                 state='published')
#             article.articleordermanager_set.create(page=self.content_holder, order=i)
#             article.tags.add(self.featured_tag)
        
#         response = self.client.get(reverse('index'))
#         for i in range(0,5):
#             self.assertContains(response, 'test article %s' % i)
    
#     def test_render_article(self):
#         """it should also render"""
#         response = self.client.get(reverse('article', kwargs={
#                                         "article_id": self.article.pk
#                                         }))
#         self.assertContains(response, 'test article')
    
#     def test_video_buy(self):
#         response = self.client.get(reverse('video', kwargs={'markup':'pml', 
#                                     'video_id': self.video.pk}))
#         self.assertContains(response, self.video_key)
    
#     def test_video_download_with_forward_lock(self):
#         # make sure the video has a file linked to it
#         tmp_file = create_temp_file('this is the tmp video file')
#         self.video.file = tmp_file.name
#         self.video.save()
        
#         response = self.client.get(
#             reverse('video_download', kwargs={'video_id': self.video.pk}), 
#             {   
#                 'key': self.video_key
#             })
        
#         tmp_file.close()
#         # make sure the video has a file object attached
#         self.assertContains(response, 'this is the tmp video file')
    
#     def test_video_download_without_forward_lock(self):
        
#         tmp_file = create_temp_file('this is the tmp video file')
#         self.video.file = tmp_file.name
#         self.video.forward_lock = False
#         self.video.save()
        
#         response = self.client.get(
#             reverse('video_download', kwargs={'video_id': self.video.pk}), 
#             {   
#                 'key': self.video_key
#             })
        
#         tmp_file.close()
#         # make sure the video has a file object attached
#         self.assertContains(response, 'this is the tmp video file')
        
    
#     def test_like_it(self):
#         for i in range(0,5):
#             response = self.client.get(reverse('likeit', kwargs={'markup':'pml', 
#                                     'article_id': self.article.pk}))
#             self.assertContains(response, 'Thank you')
#         self.assertEquals(5, LikeIt.objects.get(article=self.article).count)
    
#     def test_usage_warning(self):
#         response = self.client.get(reverse('usage_warning'), {
#             'url': 'http://some.domain/',
#             'name': 'some name'
#         })
#         self.assertContains(response, 'Attention')
#         self.assertContains(response, 'http://some.domain/')
    
#     def test_quiz_post(self):
#         for i in range(0,10):
#             question = Question.objects.create(quiz=self.quiz, number=i, title='question %s' % i)
#             correct_answer = Answer.objects.create(correct_answer=True, 
#                             short_answer='yes', longer_answer='That is correct', 
#                             question=question, number=i, title='correct answer %s' % i)
#             incorrect_answer = Answer.objects.create(correct_answer=False, 
#                                 short_answer='no', longer_answer='That is incorrect', 
#                                 question=question, number=i, title='incorrect answer %s' % i)
        
#         # no answers
#         response = self.client.get(reverse('quiz_post', kwargs={
#             'markup': 'pml',
#             'quiz_id': self.quiz.pk
#         }))
#         self.assertContains(response, 'You have not answered any questions')
        
#         # 40% answered correctly, 40% incorrect, 20% unanswered
#         answers = {}
#         boolean = True
#         all_questions = self.quiz.question_set.all()
#         for question in all_questions[:8]:
#             boolean = not boolean # flip boolean
#             possible_answers = question.answer_set.filter(correct_answer=boolean)
#             answers[question.pk] = possible_answers.latest('pk').pk
        
#         # don't answer 20%
#         for question in all_questions[8:]:
#             answers[question.pk] = ''
        
#         response = self.client.get(reverse('quiz_post', kwargs={
#             'markup': 'pml',
#             'quiz_id': self.quiz.pk,
#         }), answers)
#         self.assertContains(response, 'That is correct', count=4)
#         self.assertContains(response, 'That is incorrect', count=4)
#         self.assertContains(response, 'No answer provided', count=2)
    
#     def test_your_story(self):
#         ysc = YourStoryCompetition.objects.create(content='')
#         # make sure form renders
#         response = self.client.get(reverse('your_story', kwargs={'competition_id': ysc.pk}))
#         self.assertTemplateUsed(response, 'pml/your_story/your_story.xml')
#         # make sure story is captured
#         response = self.client.get(reverse('your_story', kwargs={'competition_id': ysc.pk}), {
#             'name': 'my name',
#             'email': 'email@address.net',
#             'text': 'my story',
#             'terms': 'true'
#         })
#         self.assertTemplateUsed(response, 'pml/your_story/your_story_success.xml')
#         self.assertTrue(YourStoryEntry.objects.count(), 1)
#         entry = YourStoryEntry.objects.latest('pk')
#         self.assertEquals(entry.name, 'my name')
#         self.assertEquals(entry.email, 'email@address.net')
#         self.assertEquals(entry.text, 'my story')
#         self.assertEquals(entry.terms, True)
    
#     def test_carousel(self):
#         daytime_banner = Banner.objects.create(title='day time', 
#                             time_on="8:00", time_off="22:00", state='published')
#         nighttime_banner = Banner.objects.create(title='night time', 
#                             time_on="22:00", time_off="8:00", state='published')
#         fulltime_banner = Banner.objects.create(title='full time', 
#                             always_on=True, state='published')
        
#         response = self.client.get(reverse('carousel'), {
#             'time': "5:00"
#         })
#         self.assertContains(response, 'night time', count=1)
#         self.assertContains(response, 'full time', count=1)
#         self.assertNotContains(response, 'day time')
        
#         response = self.client.get(reverse('carousel'), {
#             'time': "17:00"
#         })
#         self.assertContains(response, 'day time', count=1)
#         self.assertContains(response, 'full time', count=1)
#         self.assertNotContains(response, 'night time')
        
#         response = self.client.get(reverse('carousel'), {
#             'time': "23:00"
#         })
#         self.assertContains(response, 'night time', count=1)
#         self.assertContains(response, 'full time', count=1)
#         self.assertNotContains(response, 'day time')
        
    
#     def test_change_alias(self):
#         response = self.client.get(reverse('change_alias', kwargs={'markup':'pml',
#                                     'article_id': self.article.pk}))
#         self.assertTemplateUsed(response, 'pml/alias/change_alias.xml')
    
#     def test_change_alias_post(self):
#         user, _ = User.objects.get_or_create(username='27761234567')
#         profile = user.get_profile()
#         self.assertNotEquals(profile.alias, 'test alias')
        
#         response = self.client.get(reverse('change_alias_post', kwargs={'markup':'pml',
#                                     'article_id': self.article.pk}), {
#                                     'alias': 'test alias'
#                                     })
#         self.assertTemplateUsed(response, 'pml/alias/change_alias_post.xml')
#         profile = reload_record(profile)
#         self.assertEquals(profile.alias, 'test alias')
    
#     def test_alias_number_filtering(self):
#         user, _ = User.objects.get_or_create(username='27761234567')
#         profile = user.get_profile()
        
#         response = self.client.get(reverse('change_alias_post', kwargs={'markup':'pml',
#                                     'article_id': self.article.pk}), {
#                                     'alias': '27761234567'
#                                     })
#         self.assertTemplateUsed(response, 'pml/alias/change_alias.xml')
#         self.assertContains(response, '27761234567 is an invalid alias')
        
#         response = self.client.get(reverse('change_alias_post', kwargs={'markup':'pml',
#                                     'article_id': self.article.pk}), {
#                                     'alias': '1234'
#                                     })
#         self.assertTemplateUsed(response, 'pml/alias/change_alias_post.xml')
#         profile = reload_record(profile)
#         self.assertEquals(profile.alias, '1234')
    
#     def test_competition(self):
#         response = self.client.get(reverse('competition', kwargs={'markup': 'pml',
#                                     'competition_id': self.competition.pk}))
#         self.assertTemplateUsed(response, 'pml/competition/competition.xml')
    
#     def test_quiz(self):
#         response = self.client.get(reverse('quiz', kwargs={'markup':'pml', 
#                                     'quiz_id': self.quiz.pk}))
#         self.assertTemplateUsed(response, 'pml/competition/quiz.xml')

# # class VideoAdminTestCase(TestCase):
# #     
# #     def setUp(self):
# #         self.va = VideoAdmin(Video, None)
# #     
# #     def tearDown(self):
# #         pass
# #     
# #     def test_video_admin_image_widget(self):
# #         dbfield, _, _, _ = Video._meta.get_field_by_name('thumbnail_1')
# #         admin_field = self.va.formfield_for_dbfield(dbfield)
# #         self.assertTrue(isinstance(admin_field.widget, AdminImageWidget))
# #     
# #     def test_video_thumbnail_generation_on_save(self):
# #         video = Video()
# #         # monkey patch
# #         video.called = False
# #         def _mp_generate_thumbnails(*args, **kwargs):
# #             video.called = True
# #         video.generate_thumbnails = _mp_generate_thumbnails
# #         self.va.save_model(None,video,None,None)
# #         self.assertTrue(video.called)
    
# class ArticleAdminTestCase(TestCase):
#     def setUp(self):
#         self.aa = ArticleAdmin(Article, None)
#         self.user = User.objects.create_user('test', 'test@domain.com', 'test')
#         self.user.is_active = True
#         self.user.is_staff = True
#         self.user.save()
#         self.article = Article.objects.create(title='')
    
#     def tearDown(self):
#         pass
    
#     def test_is_featured_display(self):
#         # not featured
#         self.assertTrue('no' in self.aa.is_featured(self.article))
#         # adding the featured tag should mark it as featured
#         self.article.tags.add(Tag.objects.create(title='featured'))
#         self.assertTrue('yes' in self.aa.is_featured(self.article))
    
#     def test_live_with(self):
        
#         client = Client()
#         client.login(username='test', password='test')
#         response = client.get(reverse('admin:live_with', kwargs={
#             'article_id': self.article.pk
#         }))
#         self.assertTemplateUsed(response, 'admin/yal/article/live_with.html')
    
#     def test_live_with_responses(self):
#         client = Client()
#         client.login(username='test', password='test')
#         response = client.get(reverse('admin:live_with_responses', kwargs={
#             'article_id': self.article.pk
#         }))
#         self.assertTemplateUsed(response, 'admin/yal/article/live_with_responses.html')
    
#     def test_vodafone_live_editor_widget(self):
#         vlew = VodafoneLiveEditorWidget()
#         html = vlew.render('key','value', attrs={"id":"id"})
#         self.assertIn('textarea', html)
#         self.assertIn('name="key"', html)
#         self.assertIn('value', html)
    
#     def test_admin_image_widget(self):
#         aiw = AdminImageWidget()
#         video = Video()
#         # if no image available it should fail gracefully & return empty string
#         self.assertEquals('', aiw.render('name', video.thumbnail_1))
#         # attach a fake file & rerender
#         video.thumbnail_1 = create_temp_file('').name
#         html = aiw.render('name', video.thumbnail_1)
#         self.assertIn('img', html)
    
# class InclusionTagTestCase(TestCase):
    
#     def setUp(self):
#         pass
        
#     def tearDown(self):
#         pass
    
