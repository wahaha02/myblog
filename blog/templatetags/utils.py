from django import template
from django.template import Library, Node
from django.contrib.sites.models import Site
from django.utils.encoding import smart_str

import myblog

register = Library()

class VarNode(Node):
    def __init__(self, var_name, var_to_resolve):
        self.var_name = var_name
        self.var_to_resolve = var_to_resolve

    def get_context(self, top_context):
        for context in top_context.dicts:
            if self.var_name in context:
                return context
        return top_context

    def render(self, context):
        try:
            resolved_var = template.resolve_variable(self.var_to_resolve,
                                                     context)
            self.get_context(context)[self.var_name] = resolved_var
        except template.VariableDoesNotExist:
            self.get_context(context)[self.var_name] = ''
        return ''

class URLNode(Node):
    def __init__(self, view_name, args, kwargs, asvar):
        self.view_name = view_name
        self.args = args
        self.kwargs = kwargs
        self.asvar = asvar

    def render(self, context):
        from django.core.urlresolvers import reverse, NoReverseMatch
        args = [arg.resolve(context) for arg in self.args]
        kwargs = dict([(smart_str(k, 'ascii'), v.resolve(context))
                       for k, v in self.kwargs.items()])


        # Try to look up the URL twice: once given the view name, and again
        # relative to what we guess is the "main" app. If they both fail, 
        # re-raise the NoReverseMatch unless we're using the 
        # {% url ... as var %} construct in which cause return nothing.
        url = ''
        try:
            url = reverse(self.view_name, args=args, kwargs=kwargs)
        except NoReverseMatch:
            project_name = settings.SETTINGS_MODULE.split('.')[0]
            try:
                url = reverse(project_name + '.' + self.view_name,
                              args=args, kwargs=kwargs)
            except NoReverseMatch:
                if self.asvar is None:
                    raise

        # Build full url path
        url = 'http://%s%s' % (Site.objects.get_current().domain, url)

        if self.asvar:
            context[self.asvar] = url
            return ''
        else:
            return url

@register.tag
def var(parser, token):
    '''
    {% var foo = expression %}
    {% var foo = Model.foo_set.count %}
    {% var foo = foo|restructuredtext %}
    {{ foo }} {{ foo|escape }}
    '''

    args = token.split_contents()
    if len(args) != 4 or args[2] != '=':
        raise template.TemplateSyntaxError(
            "'%s' statement requires the form {% %s foo = bar %}." % (
                args[0], args[0]))
    return VarNode(args[1], args[3])

@register.tag
def fullurl(parser, token):
    """
    Returns an absolute URL matching given view with its parameters.

    This is a way to define links that aren't tied to a particular URL
    configuration::

        {% url path.to.some_view arg1,arg2,name1=value1 %}

    The first argument is a path to a view. It can be an absolute python path
    or just ``app_name.view_name`` without the project name if the view is
    located inside the project.  Other arguments are comma-separated values
    that will be filled in place of positional and keyword arguments in the
    URL. All arguments for the URL should be present.

    For example if you have a view ``app_name.client`` taking client's id and
    the corresponding line in a URLconf looks like this::

        ('^client/(\d+)/$', 'app_name.client')

    and this app's URLconf is included into the project's URLconf under some
    path::

        ('^clients/', include('project_name.app_name.urls'))

    then in a template you can create a link for a certain client like this::

        {% url app_name.client client.id %}

    The URL will look like ``/clients/client/123/``.
    """
    bits = token.contents.split(' ')
    if len(bits) < 2:
        raise template.TemplateSyntaxError("'%s' takes at least one argument"
                                  " (path to a view)" % bits[0])
    viewname = bits[1]
    args = []
    kwargs = {}
    asvar = None

    if len(bits) > 2:
        bits = iter(bits[2:])
        for bit in bits:
            if bit == 'as':
                asvar = bits.next()
                break
            else:
                for arg in bit.split(","):
                    if '=' in arg:
                        k, v = arg.split('=', 1)
                        k = k.strip()
                        kwargs[k] = parser.compile_filter(v)
                    elif arg:
                        args.append(parser.compile_filter(arg))
    return URLNode(viewname, args, kwargs, asvar)
