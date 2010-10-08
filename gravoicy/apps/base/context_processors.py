# -*- coding: utf-8 -*-
from django.conf import settings

def base_context(request):
    """
    Base Settings to Context
    """
    return {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_SUB_NAME': settings.SITE_SUB_NAME,
    }
