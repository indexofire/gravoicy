# -*- coding: utf-8 -*-
import os
from settings import PROJECT_PATH


ADMINS = (
    ('Mark Renton', 'indexofire@gmail.com'),
)
MANAGERS = ADMINS

SITE_ID = 1
USE_I18N = True
USE_L10N = False

MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/media/admin/'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.csrf',
    'apps.base.context_processors.base_context',
)
ROOT_URLCONF = 'gravoicy.urls'
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.comments',
)
THEME_PATH = 'default'
TEMPLATE_DIRS = (
    #os.path.join(PROJECT_PATH, 'templates/'),
    os.path.join(PROJECT_PATH, 'templates/%s/templates/' % THEME_PATH),
)
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'templates/%s/media/' % THEME_PATH)
LANGUAGES = (
    ('zh-cn', 'Chinese'),
    ('en', 'English'),
)
TINYMCE_JS_URL = MEDIA_URL + 'global/js/tiny_mce/tiny_mce.js'
