# -*- coding: utf-8 -*-
import os
from settings import PROJECT_PATH
from settings import INSTALLED_APPS

DEBUG = True
TEMPLATE_DEBUG = DEBUG

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

INSTALLED_APPS += (
    'registration',
    'taggit',
    'voting',
    'blog',
    #'forum',
    'cms',
    #'wiki',
)
