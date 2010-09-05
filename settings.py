# Django settings for myblog project.

import sys
import os.path
from os.path import join

myblog_path = os.path.dirname(os.path.abspath(__file__))
myproject_path = myblog_path
sys.path.insert(0, myproject_path)
sys.path.insert(0, myblog_path)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'postgresql_psycopg2'
DATABASE_NAME = 'yourdatabase'
DATABASE_USER = 'yourname'
DATABASE_PASSWORD = 'yourpassword'
DATABASE_HOST = ''
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

WEB_SITE = 'http://guobudong.alwaysdata.net/'
WEB_TITLE = "Guobudong Online"

ROOT_URL = '/'
LOGIN_URL = ROOT_URL + 'login/'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = join(myblog_path, 'public', 'resources', 'static')
ADMIN_MEDIA_ROOT = join(MEDIA_ROOT, 'admin')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ROOT_URL + 'resources/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = ROOT_URL + 'media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '5u-wpkov*u3zeiuj#$%pg4mds$e(8^uo)u=#xbl%pxi&f@!0p8'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'myblog.pingback.middleware.PingbackMiddleware',
    'myblog.middleware.SetRemoteAddrFromForwardedFor',
)

ROOT_URLCONF = 'myblog.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'myblog.blog',
    'myblog.tagging',
    'myblog.comments',
    'myblog.pagination',
    'myblog.django_xmlrpc',
    'myblog.pingback',
    'myblog.rabidratings',
    'myblog.south',
)
#Akisment
AKISMET_API_KEY = ''

#Pagination
OBJECTS_PER_PAGE = 12

#tagging
FORCE_LOWERCASE_TAGS = True

DIRECTORY_URLS = (
    'http://ping.blogs.yandex.ru/RPC2',
    'http://rpc.technorati.com/rpc/ping',
)
