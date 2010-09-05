import datetime
from django.db import models
from django.conf import settings
from django.core import urlresolvers
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.utils import encoding, html
from django.utils.html import urlquote
from django.utils.translation import ugettext_lazy as _
from django.db.models.fields.files import ImageFieldFile
from managers import CommentManager
from signals import comment_was_posted, comment_save

# Create your models here.
COMMENT_MAX_LENGTH = getattr(settings, 'COMMENT_MAX_LENGTH', 3000)
COMMENT_MAX_DEPTH = getattr(settings, 'COMMENT_MAX_DEPTH', 5)

class Comment(models.Model):
    """
    A user comment about some object.
    """
    content_type   = models.ForeignKey(ContentType)
#            related_name="content_type_set_for_%(class)s")
    object_pk      = models.PositiveIntegerField(_('object id'))
    content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")
    site        = models.ForeignKey(Site, related_name="comment for %(class)s")
    
    # Who posted this comment? If ``user`` is set then it was an authenticated
    # user; otherwise at least user_name should have been set and the comment
    # was posted by a non-authenticated user.
    user        = models.ForeignKey(User, blank=True, null=True)
#            related_name="%(class)s_comments")
    user_name   = models.CharField(_("user's name"), max_length = 50, blank = True)
    user_email  = models.EmailField(_("user's email address"), blank = True)
    user_url    = models.URLField(_("user's URL"), blank = True)

    content = models.TextField(_('Content'), max_length=COMMENT_MAX_LENGTH)
    parent = models.ForeignKey('self', null = True, 
                                       blank = True, 
                                       default = None, 
                                       related_name = 'children')
    mail_notify = models.BooleanField(default = False)

    # Metadata about the comment
    date = models.DateTimeField(_('date/time submitted'), default=None)
    ip_address  = models.IPAddressField(_('IP address'), blank=True, null=True)
    is_public   = models.BooleanField(_('is public'), default=True,
                    help_text=_('Uncheck this box to make the comment effectively ' \
                                'disappear from the site.'))
    is_removed  = models.BooleanField(_('is removed'), default=False,
                    help_text=_('Check this box if the comment is inappropriate. ' \
                                'A "This comment has been removed" message will ' \
                                'be displayed instead.'))

    # Manager
    objects = CommentManager()

    class Meta:
        ordering = ('date',)
        permissions = [("can_moderate", "Can moderate comments")]
        
    def get_content_object_url(self):
        """
        Get a URL suitable for redirecting to the content object.
        """
        model = ContentType.objects.get(pk = self.content_type_id).model_class()
        object = model.objects.get(pk = self.object_pk)
        return object.get_absolute_url()

    def get_content_object_title(self):
        model = ContentType.objects.get(pk = self.content_type_id).model_class()
        object = model.objects.get(pk = self.object_pk)
        return object.title

    def __unicode__(self):
        return "%s: %s..." % (self.name, self.content[:50])

    def save(self, force_insert=False, force_update=False):
        if self.date is None:
            self.date = datetime.datetime.now()
        super(Comment, self).save(force_insert, force_update)
        comment_save.send(sender = self.__class__, comment = self, object = self.object)

    def has_parent(self):
        return bool(self.parent_id)

    def get_parent(self):
        if self.parent_id:
            return Comment.objects.get(pk = self.parent_id)
        else:
            return None

    def get_depth(self):
        def _get_depth(object, list):
            if object.has_parent():
                parent = object.get_parent()
                list.append(parent)
                _get_depth(parent, list)

        list = [1]
        _get_depth(self, list)

        return len(list)

    def get_parity(self):
        def _get_depth_odd(object):
            comments = list(Comment.objects.filter(content_type = object.content_type, 
                        object_pk = object.object_pk))
            for comment in comments:
                if comment.get_depth() != object.get_depth():
                    comments.remove(comment)

            if object.has_parent():
                parent = object.get_parent()
                podd = _get_depth_odd(parent)
                return bool((podd + 1) % 2)

            return bool((comments.index(object) + 1) % 2)

        if _get_depth_odd(self):
            return 'even'
        else:
            return 'odd'

    def is_last_child(self):
        '''Check whether this is the last child'''
        def get_root(object):
            if object.has_parent():
                return get_root(object.get_parent())
            else:
                return object

        def get_inherit(object, list):
            if object and object.has_children():
                for child in object.get_children():
                    if child.has_children():
                        list.append(child)
                        get_inherit(child, list)
                    else:
                        list.append(child)

        list = []
        last = True
        get_inherit(get_root(self), list)
        for item in list:
            if self.date < item.date:
                last = False
                break

        return last

    def has_children(self):
        return bool(self.children.get_children_by_id(self.id))

    def get_children(self):
        return self.children.get_children_by_id(self.id)

    def _get_userinfo(self):
        """
        Get a dictionary that pulls together information about the poster
        safely for both authenticated and non-authenticated comments.

        This dict will have ``name``, ``email``, and ``url`` fields.
        """
        if not hasattr(self, "_userinfo"):
            self._userinfo = {
                "name"  : self.user_name,
                "email" : self.user_email,
                "url"   : self.user_url
            }
            if self.user_id:
                u = self.user
                if u.email:
                    self._userinfo["email"] = u.email

                # If the user has a full name, use that for the user name.
                # However, a given user_name overrides the raw user.username,
                # so only use that if this comment has no associated name.
                if u.get_full_name():
                    self._userinfo["name"] = self.user.get_full_name()
                elif not self.user_name:
                    self._userinfo["name"] = u.username
        return self._userinfo
    userinfo = property(_get_userinfo, doc=_get_userinfo.__doc__)

    def _get_name(self):
        return self.userinfo["name"]
    def _set_name(self, val):
        if self.user_id:
            raise AttributeError(_("This comment was posted by an authenticated "\
                                   "user and thus the name is read-only."))
        self.user_name = val
    name = property(_get_name, _set_name, doc="The name of the user who posted this comment")
    def _get_object(self):
        model = ContentType.objects.get(pk = self.content_type_id).model_class()
        object = model.objects.get(pk = self.object_pk)
        return object
    object = property(_get_object)

    def _get_email(self):
        return self.userinfo["email"]
    def _set_email(self, val):
        if self.user_id:
            raise AttributeError(_("This comment was posted by an authenticated "\
                                   "user and thus the email is read-only."))
        self.user_email = val
    email = property(_get_email, _set_email, doc="The email of the user who posted this comment")

    def _get_url(self):
        return self.userinfo["url"]
    def _set_url(self, val):
        self.user_url = val
    url = property(_get_url, _set_url, doc="The URL given by the user who posted this comment")

    def get_absolute_url(self, anchor_pattern="#comment-%(id)s"):
        return self.get_content_object_url() + (anchor_pattern % self.__dict__)

    def get_admin_url(self):
        return '/admin/comments/comment/%d/' % self.id

    def get_as_text(self):
        """
        Return this comment as plain text.  Useful for emails.
        """
        d = {
            'user': self.user,
            'date': self.date,
            'comment': self.content,
            'domain': self.site.domain,
            'url': self.get_absolute_url()
        }
        return _('Posted by %(user)s at %(date)s\n\n%(comment)s\n\nhttp://%(domain)s%(url)s') % d

def on_comment_was_posted(sender, comment, request, *args, **kwargs):
    try:
        from akismet import Akismet
        from akismet import AkismetError
    except:
        return

    if hasattr(settings, 'AKISMET_API_KEY'):
        ak = Akismet(
            key = settings.AKISMET_API_KEY,
            blog_url='http://%s/' % Site.objects.get(pk=settings.SITE_ID).domain
        )
    else:
        return

    try:
        if ak.verify_key():
            data = {
                'user_ip': request.META.get('REMOTE_ADDR', '127.0.0.1'),
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                'referrer': request.META.get('HTTP_REFERER', ''),
                'comment_type': 'comment',
                'comment_author': comment.user_name.encode('utf-8'),
            }

            if ak.comment_check(comment.content.encode('utf-8'), data=data, build_data=True):
                comment.is_public = False
                comment.save()
    except AkismetError:
        comment.save()

comment_was_posted.connect(on_comment_was_posted)
