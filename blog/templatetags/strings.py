# coding: utf-8
from django.template import Library
from myblog.settings import WEB_SITE, WEB_TITLE

register = Library()

@register.simple_tag
def webtitle():
    return WEB_TITLE

@register.simple_tag
def website():
    return WEB_SITE
