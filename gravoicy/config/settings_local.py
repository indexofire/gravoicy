# -*- coding: utf-8 -*-
import os
from settings import PROJECT_PATH
from config.settings_base import *


DEBUG = True
TEMPLATE_DEBUG = DEBUG
SECRET_KEY = '1F=(lta=1R9je3ze@g#fa^m#hJu^mv%@8+%fZ5p)*1$(*tvbh6'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '../../grav_data.db',
        'OPTIONS': {
            'timeout': 10,
        }
    }
}
FEINCMS_ADMIN_MEDIA = '/media/feincms/'
TIME_ZONE = 'Asia/Shanghai'
LANGUAGE_CODE = 'zh-cn'

INTERNAL_IPS = (
    '127.0.0.1',
)
MIDDLEWARE_CLASSES += (
    'pagination.middleware.PaginationMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
TEMPLATE_CONTEXT_PROCESSORS += (
    'forum.context_processors.page_size',
)
INSTALLED_APPS += (
    'registration',
    'base',
    #'taggit',
    #'voting',
    'blog',
    'forum',
    #'cms',
    #'wiki',
    'debug_toolbar',
    #'redis_sessions',
    'feincms',
    'feincms.module.page',
    'feincms.module.medialibrary',
    'mptt',
    'attachments',
    'simpleavatar',
    'userprofile',
    'pagination',
)
FEINCMS_TREE_EDITOR_INCLUDE_ANCESTORS = True
#SESSION_ENGINE = 'utils.sessions.backends.redis'

FORUM_CTX_CONFIG = {
    'FORUM_TITLE': 'HZCDCLabs Forum',
    'FORUM_SUB_TITLE': '',
    'FORUM_PAGE_SIZE': 50,
    'TOPIC_PAGE_SIZE': 2,
}
SITE_NAME = 'HZCDC'
SITE_SUB_NAME = 'Labs'
MARKUP_CODE_HIGHTLIGHT = True
MARKITUP_JS_URL = '/media/markitup/sets/default/set.js'
