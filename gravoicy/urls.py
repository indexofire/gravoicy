# -*- coding: utf-8 -*-
import os
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from settings import PROJECT_PATH

admin.autodiscover()

urlpatterns = patterns('',
    # the FeinCMS frontend editing:
    url(r'admin/page/page/jsi18n/', 'django.views.generic.simple.redirect_to',
        {'url': '/admin/jsi18n/'}),
    (r'^admin/', include(admin.site.urls)),
    url(r'^preview/(?P<page_id>\d+)/', 'feincms.views.base.preview_handler', 
        name='feincms:preview'),
    # This entry is here strictly for application content testing
    # XXX this really needs to go into a URLconf file which is only used by the
    # application content testcases
    #url(r'^(.*)/$', 'feincms.views.applicationcontent.handler'),
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
