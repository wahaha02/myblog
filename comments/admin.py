from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from models import Comment

class CommentsAdmin(admin.ModelAdmin):
    fieldsets = (
        (None,
           {'fields': ('content_type', 'object_pk', 'site')}
        ),
        (_('Content'),
           {'fields': ('user', 'user_name', 'user_email', 'user_url', 'content')}
        ),
        (_('Metadata'),
           {'fields': ('date', 'ip_address', 'is_public', 'is_removed', 'parent', 'mail_notify')}
        ),
     )

    list_display = ('name', 'content_type', 'object_pk', 'ip_address', 'date', 'is_public', 'is_removed')
    list_filter = ('date', 'is_public', 'is_removed')
    date_hierarchy = 'date'
    ordering = ('-date',)
    search_fields = ('content', 'user__username', 'user_name', 'user_email', 'user_url', 'ip_address')

admin.site.register(Comment, CommentsAdmin)
