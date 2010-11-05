# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from account.views import *


urlpatterns = patterns('',
    url(r'^$', profile_list, name='profile_list'),
    (r'^', include('registration.backends.default.urls')),
    url(r'^(?P<username>\w+)/$', profile_detail, name='profile_detail'),
    url(r'^(?P<username>\w+)/edit/$', profile_edit, name='profile_edit'),
)
