from django.contrib import admin
from jmbovideos.models import Video
from django.contrib.admin.widgets import AdminFileWidget


class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'thumbnail_display', 'view_count', 'last_view_date')
    fields = (
        'featured',
        'published',
        'publish_on',
        'title',
        'description',
        'video',
        'thumbnail',
        'comments_enabled',
        'sites',
    )

    def thumbnail_display(self, video):
         return u'''
            <div align="center" href="%s" target="_blank">
                <img src="%s" alt="%s" />
            </div>''' % (video.video.url, video.thumbnail.url, video.title)
    thumbnail_display.allow_tags = True

admin.site.register(Video, VideoAdmin)