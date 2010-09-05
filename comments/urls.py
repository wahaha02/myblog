from django.conf.urls.defaults import *

urlpatterns = patterns('myblog.comments.views',
    url(r'^post/$', 'post_comment', name='comment-post-comment'),
)
