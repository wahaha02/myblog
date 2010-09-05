# coding: utf-8
from django.http import HttpResponse
from myblog.settings import WEB_TITLE

class MaintainMiddleware(object):
    def process_request(self, request):
        if not request.path == '/admin/' and not request.user.is_authenticated():
            return HttpResponse('''<head><title>%s 备份中...</title></head>
            <body>
            <h1 style="color:blue">%s 备份中</h1>
            <h2>不要走开，马上回来。</h2>
            <p align="right">%s</p>
            <p align="right">Jun 17, 2010</p>
            </body>''' % (WEB_TITLE, WEB_TITLE, WEB_TITLE))
