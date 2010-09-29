# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^blog/', include('blog.urls')),
    #(r'^cms/', include('cms.urls')),
    #(r'^forum/', include('forum.urls')),
    #(r'^wiki/', include('wiki.urls')),
)

if settings.DEBUG:
	urlpatterns += patterns('',
	    url(r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT,},
        ),
    )
