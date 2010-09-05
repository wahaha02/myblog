from django import template
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import smart_unicode
from django.utils.html import linebreaks

from myblog.comments.models import Comment
from myblog.comments.forms import CommentForm

COMMENT_MAX_DEPTH = getattr(settings, 'COMMENT_MAX_DEPTH', 5)

register = template.Library()

class BaseCommentNode(template.Node):
    """
    Base helper class (abstract) for handling the get_comment_* template tags.
    Looks a bit strange, but the subclasses below should make this a bit more
    obvious.
    """

    @classmethod
    def handle_token(cls, parser, token):
        """Class method to parse get_comment_list/count/form and return a Node."""
        tokens = token.contents.split()
        if tokens[1] != 'for':
            raise template.TemplateSyntaxError("Second argument in %r tag must be 'for'" % tokens[0])

        # {% get_whatever for obj as varname %}
        if len(tokens) == 5:
            if tokens[3] != 'as':
                raise template.TemplateSyntaxError("Third argument in %r must be 'as'" % tokens[0])
            # contentype parser.compile_filter(tokens[2]),
            # as_variable tokens[4]
            return cls(
                object_expr=parser.compile_filter(tokens[2]),
                as_varname=tokens[4],
            )

        # {% get_whatever for app.model pk as varname %}
        elif len(tokens) == 6:
            if tokens[4] != 'as':
                raise template.TemplateSyntaxError("Fourth argument in %r must be 'as'" % tokens[0])
            return cls(
                ctype=BaseCommentNode.lookup_content_type(tokens[2], tokens[0]),
                object_pk_expr=parser.compile_filter(tokens[3]),
                as_varname=tokens[5]
            )

        else:
            raise template.TemplateSyntaxError("%r tag requires 4 or 5 arguments" % tokens[0])

    @staticmethod
    def lookup_content_type(token, tagname):
        try:
            app, model = token.split('.')
            return ContentType.objects.get(app_label=app, model=model)
        except ValueError:
            raise template.TemplateSyntaxError("Third argument in %r must be in the format 'app.model'" % tagname)
        except ContentType.DoesNotExist:
            raise template.TemplateSyntaxError("%r tag has non-existant content-type: '%s.%s'" % (tagname, app, model))

    def __init__(self, ctype=None, object_pk_expr=None, object_expr=None, as_varname=None, comment=None):
        if ctype is None and object_expr is None:
            raise template.TemplateSyntaxError("Comment nodes must be given either a literal object or a ctype and object pk.")
        self.comment_model = Comment
        self.as_varname = as_varname
        self.ctype = ctype
        self.object_pk_expr = object_pk_expr
        self.object_expr = object_expr
        self.comment = comment

    def render(self, context):
        qs = self.get_query_set(context)
        context[self.as_varname] = self.get_context_value_from_queryset(context, qs)
        return ''

    def get_query_set(self, context):
        ctype, object_pk = self.get_target_ctype_pk(context)
        if not object_pk:
            return self.comment_model.objects.none()

        qs = self.comment_model.objects.filter(
            content_type=ctype,
            object_pk=smart_unicode(object_pk),
            site__pk=settings.SITE_ID,
            is_public=True,
        )
        if getattr(settings, 'COMMENTS_HIDE_REMOVED', True):
            qs = qs.filter(is_removed=False)

        return qs

    def get_target_ctype_pk(self, context):
        if self.object_expr:
            try:
                obj = self.object_expr.resolve(context)
            except template.VariableDoesNotExist:
                return None, None
            return ContentType.objects.get_for_model(obj), obj.pk
        else:
            return self.ctype, self.object_pk_expr.resolve(context, ignore_failures=True)

    def get_context_value_from_queryset(self, context, qs):
        """Subclasses should override this."""
        raise NotImplementedError

class CommentListNode(BaseCommentNode):
    """Insert a list of comments into the context."""
    def get_context_value_from_queryset(self, context, qs):
        return self.comment_model.objects.get_sorted_comments(qs)

class CommentCountNode(BaseCommentNode):
    """Insert a count of comments into the context."""
    def get_context_value_from_queryset(self, context, qs):
        return qs.count()

class CommentFormNode(BaseCommentNode):
    """Insert a form for the comment model into the context."""

    def get_form(self, context):
        ctype, object_pk = self.get_target_ctype_pk(context)
        initial_date = context['comment_meta']

        if object_pk:
            return CommentForm(ctype.get_object_for_this_type(pk=object_pk), initial=initial_date)
        else:
            return None

    def render(self, context):
        context[self.as_varname] = self.get_form(context)
        return ''

class RenderCommentFormNode(CommentFormNode):
    """Render the comment form directly"""

    @classmethod
    def handle_token(cls, parser, token):
        """Class method to parse render_comment_form and return a Node."""
        tokens = token.contents.split()
        if tokens[1] != 'for':
            raise template.TemplateSyntaxError("Second argument in %r tag must be 'for'" % tokens[0])

        # {% render_comment_form for obj %}
        if len(tokens) == 3:
            return cls(object_expr=parser.compile_filter(tokens[2]))

        # {% render_comment_form for app.models pk %}
        elif len(tokens) == 4:
            return cls(
                ctype=BaseCommentNode.lookup_content_type(tokens[2], tokens[0]),
                object_pk_expr=parser.compile_filter(tokens[3])
            )

    def render(self, context):
        ctype, object_pk = self.get_target_ctype_pk(context)
        if object_pk:
            template_search_list = [
                "comment/%s/%s/form.html" % (ctype.app_label, ctype.model),
                "comment/%s/form.html" % ctype.app_label,
                "comment/form.html"
            ]
            context.push()
            formstr = render_to_string(template_search_list, {"form" : self.get_form(context)}, context)
            context.pop()
            return formstr
        else:
            return ''

class ThreadedCommentNode(BaseCommentNode):
    @classmethod
    def handle_token(cls, parser, token):
        """Class method to parse render_comment_form and return a Node."""
        tokens = token.contents.split()
        if tokens[1] != 'for':
            raise template.TemplateSyntaxError("Second argument in %r tag must be 'for'" % tokens[0])

        # {% render_comment_form for obj %}
        if len(tokens) == 3:
            return cls(object_expr=parser.compile_filter(tokens[2]))

        # {% render_comment_form for app.models pk %}
        elif len(tokens) == 4:
            return cls(
                ctype=BaseCommentNode.lookup_content_type(tokens[2], tokens[0]),
                object_pk_expr=parser.compile_filter(tokens[3])
            )

    def render2(self, context):
        qs = self.get_query_set(context)
        comments = list(qs)

        previously_parity = {}
        def get_even_or_odd(comment, dict=previously_parity):
            def do_even_or_odd(comment, dict):
                if comment.has_parent():
                    depth = comment.get_depth()
                    if depth not in dict:
                        dict[depth] = not dict[depth - 1]

                    return dict[depth]
                else:
                    if 1 in dict:
                        previous = dict[1]
                        dict.clear()
                        dict[1] = not previous
                    else:
                        dict[1] = True

                    return dict[1]

            if do_even_or_odd(comment, dict):
                return 'even'
            else:
                return 'odd'

        def append_comment_start(comment, list, html):
            commentmeta = {
                    'id': comment.id,
                    'url': comment.get_absolute_url(),
                    'name': comment.user_name,
                    'user_url': comment.user_url,
                    'date': comment.date.strftime('%Y %B %d, %H:%M'),
                    'depth': comment.get_depth(),
                    'edit': comment.get_admin_url(),
                    'content': linebreaks(comment.content),
#                    'parity': comment.get_parity(),
                    'parity': get_even_or_odd(comment),
                }
            if not comment.has_parent():
                #TODO author's comment
                html.append('<li class="comment %(parity)s thread-%(parity)s depth-%(depth)d" id="comment-%(id)d">\n' % commentmeta)
            else:
                html.append('<li class="comment %(parity)s depth-%(depth)d" id="comment-%(id)d">\n' % commentmeta)

            if commentmeta['user_url']:
                html.append('<div id="div-comment-%(id)d"><div class="comment-author vcard"><cite><a href="%(user_url)s" rel="external nofollow">%(name)s</a></cite></div>\n' % commentmeta)
            else:
                html.append('<div id="div-comment-%(id)d"><div class="comment-author vcard">%(name)s</div>\n' % commentmeta)

            if context['user'].is_staff:
                html.append('<div class="comment-meta commentmetadata"><a href="%(url)s">%(date)s</a>&nbsp;&nbsp;<a href="%(edit)s" title="Edit comment">Edit</a></div>\n'
                   '<p>%(content)s</p>\n' % commentmeta)
            else:
                html.append('<div class="comment-meta commentmetadata"><a href="%(url)s">%(date)s</a></div>\n'
                   '<p>%(content)s</p>\n' % commentmeta)

            if comment.get_depth() < COMMENT_MAX_DEPTH:
                html.append('<div class="reply"><a rel="nofollow" href="%(url)s#respond" onclick=\'return addComment.moveForm("div-comment-%(id)d", "%(id)d", "respond")\'>Reply</a></div></div>\n\n' % commentmeta)

        def append_comment_end(html):
            html.append('</li>\n')

        def append_child_start(html):
            html.append('<ul class="children">\n')

        def append_child_end(html):
            html.append('</ul>\n')

        def create_comment_html(root, list, html):
            append_comment_start(root, list, html)
            list.remove(root)
            if root.has_children():
                children = root.get_children()
                for child in children:
                    append_child_start(html)
                    create_comment_html(child, list, html)

            append_comment_end(html)
            if root.has_parent():
                append_child_end(html)

            if len(list) > 0 and not root.has_parent():
                create_comment_html(list[0], list, html)

        html = []
        if comments:
            sorted = []
            first = comments[0]
            html.append('<ol class="commentlist">\n')
            create_comment_html(first, comments, html)
            html.append('</ol>')

        return ''.join(html)

    def render(self, context):
        qs = self.get_query_set(context)
        comments = list(qs)

        previously_parity = {}
        def get_even_or_odd(comment, dict=previously_parity):
            def do_even_or_odd(comment, dict):
                if comment.has_parent():
                    depth = comment.get_depth()
                    if depth not in dict:
                        dict[depth] = not dict[depth - 1]

                    return dict[depth]
                else:
                    if 1 in dict:
                        previous = dict[1]
                        dict.clear()
                        dict[1] = not previous
                    else:
                        dict[1] = True

                    return dict[1]

            if do_even_or_odd(comment, dict):
                return 'even'
            else:
                return 'odd'

        def append_comment_start(comment, list, html):
            commentmeta = {
                    'id': comment.id,
                    'url': comment.get_absolute_url(),
                    'name': comment.user_name,
                    'user_url': comment.user_url,
                    'date': comment.date.strftime('%Y %B %d, %H:%M'),
                    'depth': comment.get_depth(),
                    'edit': comment.get_admin_url(),
                    'content': linebreaks(comment.content),
#                    'parity': comment.get_parity(),
                    'parity': get_even_or_odd(comment),
                }
            if not comment.has_parent():
                #TODO author's comment
                html.append('<li class="comment %(parity)s thread-%(parity)s depth-%(depth)d" id="comment-%(id)d">\n' % commentmeta)
            else:
                html.append('<li class="comment %(parity)s depth-%(depth)d" id="comment-%(id)d">\n' % commentmeta)

            if commentmeta['user_url']:
                html.append('<div id="div-comment-%(id)d"><div class="comment-author vcard"><cite><a href="%(user_url)s" rel="external nofollow">%(name)s</a></cite></div>\n' % commentmeta)
            else:
                html.append('<div id="div-comment-%(id)d"><div class="comment-author vcard">%(name)s</div>\n' % commentmeta)

            if context['user'].is_staff:
                html.append('<div class="comment-meta commentmetadata"><a href="%(url)s">%(date)s</a>&nbsp;&nbsp;<a href="%(edit)s" title="Edit comment">Edit</a></div>\n'
                   '<p>%(content)s</p>\n' % commentmeta)
            else:
                html.append('<div class="comment-meta commentmetadata"><a href="%(url)s">%(date)s</a></div>\n'
                   '<p>%(content)s</p>\n' % commentmeta)

            if comment.get_depth() < COMMENT_MAX_DEPTH:
                html.append('<div class="reply"><a rel="nofollow" href="%(url)s#respond" onclick=\'return addComment.moveForm("div-comment-%(id)d", "%(id)d", "respond")\'>Reply</a></div></div>\n\n' % commentmeta)

        def append_comment_end(html):
            html.append('</li>\n')

        def append_child_start(html):
            html.append('<ul class="children">\n')

        def append_child_end(html):
            html.append('</ul>\n')

        def create_comment_html(root, list, html):
            append_comment_start(root, list, html)
            list.remove(root)
            if root.has_children():
                children = root.get_children()
                for child in children:
                    append_child_start(html)
                    create_comment_html(child, list, html)

            append_comment_end(html)
            if root.has_parent():
                append_child_end(html)

            if len(list) > 0 and not root.has_parent():
                create_comment_html(list[0], list, html)

        html = []
        if comments:
            sorted = []
            first = comments[0]
            html.append('<ol class="commentlist">\n')
            create_comment_html(first, comments, html)
            html.append('</ol>')

        return ''.join(html)

@register.tag
def get_comment_count(parser, token):
    """
    Gets the comment count for the given params and populates the template
    context with a variable containing that value, whose name is defined by the
    'as' clause.

    Syntax::

        {% get_comment_count for [object] as [varname]  %}
        {% get_comment_count for [app].[model] [object_id] as [varname]  %}

    Example usage::

        {% get_comment_count for event as comment_count %}
        {% get_comment_count for calendar.event event.id as comment_count %}
        {% get_comment_count for calendar.event 17 as comment_count %}

    """
    return CommentCountNode.handle_token(parser, token)

@register.tag
def get_comment_list(parser, token):
    """
    Gets the list of comments for the given params and populates the template
    context with a variable containing that value, whose name is defined by the
    'as' clause.

    Syntax::

        {% get_comment_list for [object] as [varname]  %}
        {% get_comment_list for [app].[model] [object_id] as [varname]  %}

    Example usage::

        {% get_comment_list for event as comment_list %}
        {% for comment in comment_list %}
            ...
        {% endfor %}

    """
    return CommentListNode.handle_token(parser, token)

@register.tag
def get_comment_form(parser, token):
    """
    Get a (new) form object to post a new comment.

    Syntax::

        {% get_comment_form for [object] as [varname] %}
        {% get_comment_form for [app].[model] [object_id] as [varname] %}
    """
    return CommentFormNode.handle_token(parser, token)

@register.tag
def render_comment_form(parser, token):
    """
    Render the comment form (as returned by ``{% render_comment_form %}``) through
    the ``comments/form.html`` template.

    Syntax::

        {% render_comment_form for [object] %}
        {% render_comment_form for [app].[model] [object_id] %}
    """
    return RenderCommentFormNode.handle_token(parser, token)

@register.simple_tag
def comment_form_target():
    """
    Get the target URL for the comment form.

    Example::

        <form action="{% comment_form_target %}" method="POST">
    """
    return 'test'

@register.tag
def get_threaded_comment_list(parser, token):
    return ThreadedCommentNode.handle_token(parser, token)
