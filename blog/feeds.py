import datetime
import time

from django.contrib.syndication.feeds import Feed
from django.contrib.sites.models import Site

import myblog
from myblog.blog.models import Post
from myblog.comments.models import Comment
from myblog.settings import WEB_SITE, WEB_TITLE


URL = 'feed-notify'

def return_url():
    return WEB_SITE + URL + '?=' + time.strftime('%m%d')

class NotifyMigrate(Feed):
    title = WEB_TITLE
    link = WEB_SITE
    description = "Hello! This is" + title
    author = 'bin.c.chen@gmail.com'
    title_template = 'feed/latest_title.html'
    description_template = 'feed/latest_description.html'

    def items(self):
        post = Post.objects.get(slug=URL)
        post.get_absolute_url = return_url
        return [post]

    def item_pubdate(self, item):
        return item.date

class LatestPosts(Feed):
    title = WEB_TITLE
    link = WEB_SITE
    description = "Hello! This is" + title
    author = 'bin.c.chen@gmail.com'
    title_template = 'feed/latest_title.html'
    description_template = 'feed/latest_description.html'

    def items(self):
        return Post.objects.get_post()[:10]

    def item_pubdate(self, item):
        return item.date

class LatestCommentFeed(Feed):
    """Feed of latest comments on the current site."""

    def title(self):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return u"%s comments" % self._site.name

    def link(self):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return "http://%s/" % (self._site.domain)

    def description(self):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return u"Latest comments on %s" % self._site.name

    def items(self):
        qs = Comment.objects.filter(
            site__pk=myblog.settings.SITE_ID,
            is_public=True,
            is_removed=False,
        )
        if getattr(myblog.settings, 'COMMENTS_BANNED_USERS_GROUP', None):
            where = ['user_id NOT IN (SELECT user_id FROM auth_user_groups WHERE group_id = %s)']
            params = [myblog.settings.COMMENTS_BANNED_USERS_GROUP]
            qs = qs.extra(where=where, params=params)
        return qs.order_by('-date')[:40]

    def item_pubdate(self, item):
        return item.date
