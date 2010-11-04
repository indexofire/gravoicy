# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from userprofile.views import *


urlpatterns = patterns('',
    url(r'^$', profile_list, name='profile_list'),
    url(r'^create/$', profile_create, name='profile_create'),
    url(r'^(?P<username>[-\w]+)/$', profile_detail, name='profile_detail'),
    url(r'^(?P<username>[-\w]+)/edit/$', profile_edit, name='profile_edit'),
)
