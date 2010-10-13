# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from article.views import *

urlpatterns = patterns('',
    url('^$', index, name='article-index'),
)
