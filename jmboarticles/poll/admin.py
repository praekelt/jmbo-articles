from django.contrib import admin


from jmboarticles.poll.models import Poll, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    readonly_fields = ('vote_count',)


class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'published', 'publish_on', 'featured',)
    filter_by = ('published', 'publish_on', 'sites', 'featured',)
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

admin.site.register(Poll, PollAdmin)
