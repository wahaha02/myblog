import os
import Image

from django.db import models
from django.utils import html
from django.conf import settings
from django.db.models import signals
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from django.db.models.fields.files import ImageFieldFile

from myblog.tagging.models import Tag
from myblog.tagging.fields import TagField
from myblog.comments.models import Comment
from myblog.comments.signals import  comment_save
from myblog.blog.managers import PostManager

class Category(models.Model):
    title = models.CharField(max_length=250, help_text=_('Maximum 250 '
            'characters.'))
    slug = models.SlugField(unique=True, help_text=_('Suggested value '
            'automatically generated from title. Must be unique.'))
    description = models.TextField()

    class Meta:
        ordering = ['title']
        verbose_name_plural = _('Categories')

    def __unicode__(self):
        return self.title

    def get_post_count(self):
        '''Return the post number under the category'''
        return Post.objects.get_post_by_category(self).count()

    @models.permalink
    def get_absolute_url(self):
        return ('post-category', [str(self.slug)])

class Post(models.Model):
    TYPE_CHOICES = (
        ('page', _('Page')),
        ('post', _('Post')),
    )
    STATUS_CHOICES = (
        ('publish', _('Published')),
        ('draft', _('Unpublished')),
    )
    COMMENT_CHOICES = (
        ('open', _('Open')),
        ('closed', _('Closed')),
    )
    title = models.CharField(max_length=64)
    slug = models.SlugField(blank=True, null=True, unique=True)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, default=0)
    category = models.ManyToManyField(Category)
    type = models.CharField(max_length=20, default='post', choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, default='publish', choices=STATUS_CHOICES)
    comments = generic.GenericRelation(Comment,
                    object_id_field='object_pk',
                    content_type_field='content_type')
    comment_status = models.CharField(max_length=20, default='open', choices=COMMENT_CHOICES)
    objects = PostManager()
    tag = TagField()

    def save(self):
        try:
            self.content = html.clean_html(self.content)
        except:
            pass
        super(Post, self).save()

        # Initial the views and comments count to 0 if the PostMeta isn't available
        pm, created = PostMeta.objects.get_or_create(post=self, meta_key='views')
        if created:
            pm.meta_value = '0'
            pm.save()

        pm, created = PostMeta.objects.get_or_create(post=self, meta_key='comments_count')
        if created:
            pm.meta_value = '0'
            pm.save()

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        if self.type == 'post':
            return ('single_post', [str(self.id)])
        else:
            return ('static_pages', [str(self.slug)])

    def get_admin_url(self):
        return '/admin/blog/post/%d/' % self.id

    def get_author(self):
        try:
            profile = self.author.get_profile()
        except Exception:
            name = self.author.username
        else:
            name = profile.nickname

        return name

    def get_views_count(self):
        return PostMeta.objects.get(post=self, meta_key='views').meta_value

    def hit_views(self):
        pm = PostMeta.objects.get(post=self, meta_key='views')
        pm.meta_value = str(int(pm.meta_value) + 1)
        pm.save()

    def get_comments_count(self):
        return PostMeta.objects.get(post=self.id, meta_key='comments_count').meta_value

    def hit_comments(self):
        pm = PostMeta.objects.get(post=self, meta_key='comments_count')
        pm.meta_value = str(self.get_comments().count())
        pm.save()

    def get_comments(self):
        return Comment.objects.for_model(self)

    def get_tags(self):
        return Tag.objects.get_for_object(self)

    def __get_excerpt(self):
        return self.content.split('<!--more-->')[0]

    excerpt = property(__get_excerpt)

    def __get_remain(self):
        return self.content.split('<!--more-->')[1]

    remain = property(__get_remain)

    def __get_pagebreak(self):
        try:
            self.content.index('<!--more-->')
        except ValueError:
            return False
        else:
            return True
    pagebreak = property(__get_pagebreak)

    def get_categories(self):
        return self.category.all()

    def is_public(self):
        if self.status == 'publish':
            return True
        else:
            return False

    @property
    def allow_comment(self):
        if self.comment_status == 'closed':
            return False
        else:
            return True

class PostMeta(models.Model):
    post = models.ForeignKey(Post)
    meta_key = models.CharField(max_length=128)
    meta_value = models.TextField()

    def __unicode__(self):
        return '<%s: %s>' % (self.meta_key, self.meta_value)

class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    nickname = models.CharField(max_length=30)
    website = models.URLField(blank=True)

    def save(self):
        if not self.nickname:
            self.nickname = self.user.username
        super(Profile, self).save()

    def __unicode__(self):
        return self.nickname

class Link(models.Model):
    url = models.URLField()
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_public = models.BooleanField(_('is public'), default=True)

    def __unicode__(self):
        return '%s: %s' % (self.name, self.url)

WATER_BIG = os.path.join(settings.MEDIA_ROOT, 'img/weblogo.png')
WATER_SMALL = os.path.join(settings.MEDIA_ROOT, 'img/weblogo_wp.png')

class Media(models.Model):
    UPLOAD_ROOT = 'uploads/%Y/%m'
    WATER_ROOT = 'pictures/%Y/%m'
    THUMB_SIZE = '640'
    LOGO_SIZE = '48'

    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to=UPLOAD_ROOT)
    watermarked = models.ImageField(blank=True, upload_to=WATER_ROOT)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = _('Media')

    def save(self, force_insert=False, force_update=False):
        super(Media, self).save(force_insert, force_update)
        base = Image.open(self.image.path)
        width, height = base.size

        if width > 400:
            logo = Image.open(WATER_BIG)
        else:
            logo = Image.open(WATER_SMALL)

        base.paste(logo, (base.size[0] - logo.size[0], base.size[1] - logo.size[1]), logo)

        water_folder = os.path.join(settings.MEDIA_ROOT, self.date.strftime(self.WATER_ROOT))
        if not os.path.exists(water_folder):
            os.makedirs(water_folder)

        relate_path = os.path.join(self.date.strftime(self.WATER_ROOT),
                                   os.path.basename(self.image.name))

        base.save(os.path.join(settings.MEDIA_ROOT, relate_path))
        self.watermarked = ImageFieldFile(self, self.watermarked, relate_path)
        super(Media, self).save(force_insert, force_update)

    def __unicode__(self):
        return _('%s %s') % (self.title, self.date.strftime('%I:%M%p, %Y/%m/%d'))

    def get_thumb_url(self):
        try:
            return self.watermarked.url
        except:
            return self.image.url

    def get_logo_url(self):
        return self.image.url + '?width=' + self.LOGO_SIZE + '&height=' + self.LOGO_SIZE

from myblog.pingback.client import ping_external_links
signals.post_save.connect(
        ping_external_links(content_attr='content', url_attr='get_absolute_url'),
        sender=Post, weak=False)

def on_comment_save(sender, comment, *args, **kwargs):
    post = comment.object
    post.hit_comments()

comment_save.connect(on_comment_save)
