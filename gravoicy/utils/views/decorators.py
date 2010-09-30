# -*- coding: utf-8 -*-
from django.conf import settings


def develop_safe(view):
    """
    This is a decorator which essentially replaces the decorated view with a
    view that always raises Http404 (File Not Found) when settings.DEBUG is
    set to True.

    The code is from:
    http://djangosnippets.org/snippets/2138/
    
    Usage:
    from utils.views.decorators import develop_safe
    
    @develop_safe
    def delete_all_users(request):
        User.objects.all().delete()
        return HttpResponse('Successfully deleted all users.')
    """
    def http_404(*args, **kwargs):
        from django.http import Http404
        raise Http404

    def inner(*args, **kwargs):
        return view(*args, **kwargs)

    if not settings.DEBUG:
        return http_404
    return inner


def render_to(template=None, mimetype="text/html"):
    """
    Decorator for Django views that sends returned dict to render_to_response 
    function.

    Template name can be decorator parameter or TEMPLATE item in returned 
    dictionary.  RequestContext always added as context instance.
    If view doesn't return dict then decorator simply returns output.

    Parameters:
      - template: template name to use
      - mimetype: content type to send in response headers

    Examples:
    # 1. Template name in decorator parameters

    @render_to('template.html')
    def foo(request):
        bar = Bar.object.all()  
        return {'bar': bar}

    # equals to 
    def foo(request):
        bar = Bar.object.all()  
        return render_to_response('template.html',
            {'bar': bar}, context_instance=RequestContext(request))


    # 2. Template name as TEMPLATE item value in return dictionary.
         if TEMPLATE is given then its value will have higher priority 
         than render_to argument.

    @render_to()
    def foo(request, category):
        template_name = '%s.html' % category
        return {'bar': bar, 'TEMPLATE': template_name}
    
    #equals to
    def foo(request, category):
        template_name = '%s.html' % category
        return render_to_response(template_name, 
            {'bar': bar}, context_instance=RequestContext(request))

    """
    def renderer(function):
        @wraps(function)
        def wrapper(request, *args, **kwargs):
            output = function(request, *args, **kwargs)
            if not isinstance(output, dict):
                return output
            tmpl = output.pop('TEMPLATE', template)
            return render_to_response(tmpl, output, \
                context_instance=RequestContext(request), mimetype=mimetype)
        return wrapper
    return renderer
