# -*- coding: utf-8 -*-
import os
from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template
from django.views.generic.simple import redirect_to
from django.contrib import admin
from settings import PROJECT_PATH


admin.autodiscover()

urlpatterns = patterns('',
    (r'^favicon\.ico$', redirect_to, {'url': '/media/favicon.ico'}),
    (r'^robots\.txt$', direct_to_template, {'template': 'robots.txt', 'mimetype': 'text/plain'}),
    (r'^avatar/', include('avatar.urls')),
    #(r'^member/', include('userprofile.urls')),
    (r'^accounts/', include('account.urls')),
    (r'^settings/', include('appsettings.urls')),
    # the FeinCMS frontend editing:
    url(r'admin/page/page/jsi18n/', 'django.views.generic.simple.redirect_to',
        {'url': '/admin/jsi18n/'}),
    (r'^admin/', include(admin.site.urls)),
    url(r'^preview/(?P<page_id>\d+)/', 'feincms.views.base.preview_handler',
        name='feincms:preview'),
    (r'^attachment/', include('attachment.urls')),
    # This entry is here strictly for application content testing
    # XXX this really needs to go into a URLconf file which is only used by the
    # application content testcases
    #url(r'^(.*)/$', 'feincms.views.applicationcontent.handler'),
    url(r'^category/', include('categories.urls')),
    url(r'^$|^(.*)/$', 'feincms.views.applicationcontent.handler'),
)
#urlpatterns = patterns('',
    #(r'^admin/', include(admin.site.urls)),
    #(r'^blog/', include('blog.urls')),
    #(r'^cms/', include('cms.urls')),
    #(r'^forum/', include('forum.urls')),
    #(r'^wiki/', include('wiki.urls')),
#)

if settings.DEBUG:
	urlpatterns += patterns('',
	    url(r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT,},
        ),
    )
