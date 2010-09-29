# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from blog.views import *


urlpatterns = patterns('',
    url(r'^$', blog_index, name='blog-index'),
    url(r'^(?P<username>[-\w]+)$', userblog_index, name='blog-index'),
    url(r'^(?P<username>[-\w]+)/page/(?P<page>\d+)/$', userblog_index, name='blog-paginated'),
    url(r'^(?P<username>[-\w]+)/category/$', category_list, name='blog-category-list'),
    url(r'^(?P<username>[-\w]+)/category/(?P<slug>[-\w]+)/$', category_detail, name='blog-category-detail'),
    url(r'^(?P<username>[-\w]+)/(?P<year>\d{4})/$', entry_year, name='blog-entry-year'),
    url(r'^(?P<username>[-\w]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/$', entry_month, name='blog-entry-month'),
)
