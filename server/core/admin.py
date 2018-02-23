from django.contrib import admin

from .models import Tag, Link


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class LinkAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'url', 'title', 'tag_list', 'user')

    def tag_list(self, obj):
        return ', '.join(obj.tags.values_list('name', flat=True))


admin.site.register(Tag, TagAdmin)
admin.site.register(Link, LinkAdmin)
