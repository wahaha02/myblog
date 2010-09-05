class SetRemoteAddrFromForwardedFor(object):
    '''Thanks http://lucentbeing.com/blog/fixing-django-comment-ips-webfaction/'''
    def process_request(self, request):
        try:
            real_ip = request.META['HTTP_X_FORWARDED_FOR']
        except KeyError:
            return None
        else:
            real_ip = real_ip.split(",")[0].strip()
            request.META['REMOTE_ADDR'] = real_ip
