from django.contrib import admin

from models import Item

class ItemAdmin(admin.ModelAdmin):
	list_display = ('title', 'publish_on', 'published',)

admin.site.register(Item, ItemAdmin)