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
        'NAME': os.path.join(PROJECT_PATH, 'database/data.sql'),
        'OPTIONS': {
            'timeout': 10,
        }
    }
}

TIME_ZONE = 'Asia/Shanghai'
LANGUAGE_CODE = 'zh-cn'

INTERNAL_IPS = (
    '127.0.0.1',
)
MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
INSTALLED_APPS += (
    'registration',
    'taggit',
    #'voting',
    #'blog',
    #'forum',
    'cms',
    #'wiki',
    'debug_toolbar',
    #'redis_sessions',
)

SESSION_ENGINE = 'utils.sessions.backends.redis'
