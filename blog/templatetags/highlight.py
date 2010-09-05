#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.template import Library
import re

DEBUG = False
register = Library()

@register.filter
def highlight_format(value):

    p_sub = re.compile('__codestart__ (\w+)')
    value = p_sub.sub(r'<pre name="code" class="\g<1>">', value)
    p_sub = re.compile(r'__codeend__', re.VERBOSE)
    value = p_sub.sub(r'</pre>', value)
    if DEBUG:
        print value
        print '+' * 80
    p_highlight = re.compile(r'(<pre name="code" class="\w+">)(?P<codeblock>.*)(</pre>)', re.S)
    f_list = p_highlight.findall(value)
    if f_list:
        s_list = p_highlight.split(value)
        if DEBUG:
            for i in s_list:
                print i
                print '=' * 80
        for code_block in p_highlight.finditer(value):
            code = code_block.group('codeblock')
            index = s_list.index(code)
            code = code.replace('&lt;', '<')
            code = code.replace('&gt;', '>')
            code = code.replace('&amp;', '&')
            code = code.replace('<p>', '')
            code = code.replace('</p>', '')
            s_list[index] = code

        value = ''.join(s_list)

    return value
