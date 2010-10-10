# -*- coding: utf-8 -*-
from django.http import HttpResponse
try:
    import simplejson
except:
    from django.utils import simplejson


def json_response(data):
    return HttpResponse(simplejson.dumps(data), mimetype='text/html')
