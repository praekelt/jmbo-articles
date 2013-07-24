from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic.simple import direct_to_template
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.db.models import Q

from jmbocomments.models import UserComment, UserCommentFlag
from jmboarticles.models import Article


def article_list(request, page=1):

    article_qs = Article.published_objects.all()

    paginator = Paginator(article_qs, per_page=8)
    try:
        page = paginator.page(page)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return direct_to_template(request, 'article/article_list.html', {
        'article_list': page.object_list,
        'page_obj': page
    })


def article_detail(request, pk, page=None):

    try:
        article = Article.objects.select_related('poll').get(pk=pk)
    except Article.DoesNotExist:
        raise Http404

    article.inc_view_count()
    article_content_type = ContentType.objects.get_for_model(Article)

    comment_qs = UserComment.objects.filter(content_type=article_content_type,
        object_pk=article.pk).select_related('user').order_by('submit_date')

    comments_per_page = 5
    if hasattr(settings, 'COMMENTS_PER_PAGE'):
        comments_per_page = settings.COMMENTS_PER_PAGE

    paginator = Paginator(comment_qs, per_page=comments_per_page, orphans=4)
    if not page:
        page = paginator.num_pages

    comment_list = paginator.page(page)
    comment_list.object_list = reversed(comment_list.object_list)
    comment_count = paginator.count

    return direct_to_template(request, 'article/article_detail.html', {
        'article': article,
        'comment_list': comment_list,
        'comment_count': comment_count,
        'current_url': reverse('article_detail', kwargs={
            'pk': article.pk,
        })
    })

def article_detail_redo(request, pk, page=1):

    try:
        article = Article.objects.select_related('poll').get(pk=pk)
    except Article.DoesNotExist:
        raise Http404

    article.inc_view_count()
    article_content_type = ContentType.objects.get_for_model(Article)

    exclude_flags = [UserCommentFlag.COMMUNITY_REMOVAL,
                     UserCommentFlag.MODERATOR_DELETION]
    comment_qs = UserComment.objects.filter(content_type=article_content_type,
                                            object_pk=article.pk)\
                                    .exclude(is_removed=True,
                                             flag_set__flag=exclude_flags)\
                                    .select_related('user')\
                                    .order_by('-submit_date')

    comments_per_page = 5
    if hasattr(settings, 'COMMENTS_PER_PAGE'):
        comments_per_page = settings.COMMENTS_PER_PAGE

    paginator = Paginator(comment_qs, comments_per_page)

    try:
        comment_list = paginator.page(page)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        comment_list = paginator.page(paginator.num_pages)

    comment_count = paginator.count

    return direct_to_template(request, 'article/article_detail.html', {
        'article': article,
        'comment_list': comment_list,
        'comment_count': comment_count,
        'current_url': reverse('article_detail_redo', kwargs={
            'pk': article.pk,
        })
    })

def article_like(request, pk):

    if request.user.is_authenticated():

        article = get_object_or_404(Article, pk=pk)
        if not request.user.liked_articles.filter(pk=article.pk).exists():
            article.like_count += 1
            article.like_users.add(request.user)
            article.save()


    return HttpResponseRedirect('../')
