# -*- coding: utf-8 -*-
import os
from settings import PROJECT_PATH


ADMINS = (
    #('admin', ''),
)
MANAGERS = ADMINS

SITE_ID = 1
USE_I18N = True
USE_L10N = False
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media/')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/media/admin/'
SECRET_KEY = '1F=(lta=1R9je3ze@g#fa^m#hJu^mv%@8+%fZ5p)*1$(*tvbh6'
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
THEME_PATH = 'default/'
TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates/%s' % THEME_PATH),
)
