from django.contrib import admin
from django.db.models import Sum

from jmboarticles.poll.models import Poll, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    readonly_fields = ('vote_count',)


class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'published', 'publish_on', 'featured',\
                    'total_votes')
    list_filter = ('published', 'publish_on', 'sites', 'featured',)
    list_editable = ('published', 'featured',)

    inlines = [ChoiceInline, ]
    fieldsets = (
        (None, {
            'fields': ('question', 'image', 'featured',
                       'published', 'publish_on',)
        }),
        (None, {
            'fields': ('sites',)
        }),
    )

    def total_votes(self, instance):
        return instance.choice_set\
                        .aggregate(Sum('vote_count'))['vote_count__sum']

admin.site.register(Poll, PollAdmin)
