from django.contrib import admin
from django.db import models
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage

from jmboarticles.models import Article
from jmbocomments.models import UserComment

from ckeditor.widgets import AdminCKEditor


class ArticleAdmin(admin.ModelAdmin):


    list_filter = ('published', 'on_homepage', 'publish_on', 'sites', 'tags', 'categories')
    list_display = ('title', 'published', 'publish_on', 'published_on', 'created',
                    'view_count', 'regions', '_view_comments')
    list_editable = ('published',)
    search_fields = ('title',)
    filter_horizontal = ('categories', 'tags')

    formfield_overrides = {
        models.TextField: {'widget': AdminCKEditor},
    }
    ordering = ('-published', '-published_on', '-updated', 'created',)
    prepopulated_fields =  {'slug': ('title',),}
    save_on_top = True
    readonly_fields = ('author', 'created', 'updated', 'published_on')
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'publish_on', 'published_on', 'on_homepage'),
        }),
        (None, {
            'fields': ('categories', 'tags', 'linked_article', 'linked_page'),
        }),
        ('Advanced', {
            'fields': ('slug',),
            'classes': ('collapse',)
        }),
        (None, {
            'fields': ('image', 'video', 'content', ('source_link', 'source_name')),
        }),
        (None, {
            'fields': ('sites', 'polls', 'downloads', 'comments_enabled',),
        }),
        (None, {
            'fields': ('author', 'created', 'updated')
        })
    )

    def regions(self, article):
        return ', '.join([site.name for site in article.sites.all()])

    def _view_comments(self, article):
        print dir(article)
        return '<a href="/admin/jmbocomments/usercomment/?object_pk=%s">View (%s)</a>' % (
            article.pk, UserComment.objects.filter(object_pk=article.pk).count())
    _view_comments.short_description = 'Comments'
    _view_comments.allow_tags = True

    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        obj.save()


class RichTextFlatPageAdmin(FlatPageAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminCKEditor}
    }

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, RichTextFlatPageAdmin)
admin.site.register(Article, ArticleAdmin)

