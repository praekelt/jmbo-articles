from django.contrib import admin
from django.db import models
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage

from jmboarticles.models import Article

from ckeditor.widgets import AdminCKEditor


class ArticleAdmin(admin.ModelAdmin):


    list_filter = ('published', 'on_homepage', 'publish_on', 'sites', 'tags', 'categories')
    list_display = ('title', 'published', 'publish_on', 'published_on', 'updated', 'created',
                    'view_count', 'last_view_date', 'regions')
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
            'fields': ('sites', 'poll', 'downloads', 'comments_enabled',),
        }),
        (None, {
            'fields': ('author', 'created', 'updated')
        })
    )

    def regions(self, article):
        return ', '.join([site.name for site in article.sites.all()])

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

