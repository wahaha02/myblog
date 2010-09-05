#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.template import Library

register = Library()

@register.inclusion_tag("tag/tag_list.html")
def show_tags_for_post(obj):
    return {"obj": obj}
