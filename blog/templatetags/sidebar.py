# coding: utf-8
import datetime

from django.utils.translation import gettext as _
from django.template import Library
from django.db import connection

from myblog.blog.models import Post, Category, Link
from myblog.comments.models import Comment
from myblog.pingback.models import Pingback

register = Library()

@register.inclusion_tag('sidebar/recent_posts.html', takes_context=True)
def get_recent_posts(context):
    #TODO Use settings to determine the latest items.
    return {'posts': Post.objects.get_post()[:15]}

@register.inclusion_tag('sidebar/recent_comments.html', takes_context=True)
def get_recent_comments(context):
    comments = Comment.objects.in_public()[:15]

    return {'comments': comments}

@register.inclusion_tag('sidebar/recent_pingbacks.html', takes_context=True)
def get_recent_pingbacks(context):
    pingbacks = Pingback.objects.all().order_by('-date')[:15]

    return {'pingbacks': pingbacks}

@register.inclusion_tag('sidebar/links.html', takes_context=True)
def get_links(context):
    links = Link.objects.all()

    return {'links': links}

@register.inclusion_tag('sidebar/category_list.html', takes_context=True)
def get_categories(context):
    return {'categories': Category.objects.all(),
        'posts': Post.objects.get_post()}

@register.inclusion_tag('sidebar/archive_list.html', takes_context=True)
def get_archive(context):
    return {'months': Post.objects.dates('date', 'month')}
