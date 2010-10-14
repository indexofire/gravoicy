# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.template import TemplateSyntaxError, RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_str, force_unicode
from django.utils.safestring import mark_safe
from content_ext.markup.forms import MarkupContentAdminForm


def restructuredtext(value):
    """
    parse restructured text
    """
    try:
        from docutils.core import publish_parts
        from docutils.parsers.rst import directives, Directive
        from content_ext.markup.directives.code import CodeHighlight
    except ImportError:
        if settings.DEBUG:
            raise TemplateSyntaxError("Error in content type: The Python "
                "docutils library isn't installed.")
        return force_unicode(value)
    else:
        docutils_settings = getattr(settings,
            'RESTRUCTUREDTEXT_FILTER_SETTINGS', {},)
        if settings.MARKUP_CODE_HIGHTLIGHT:
            directives.register_directive('code', CodeHighlight)
        parts = publish_parts(source=smart_str(value), writer_name="html4css1",
            settings_overrides=docutils_settings,)
        return mark_safe(force_unicode(parts["html_body"]))

def markdown(value):
    """
    Runs Markdown over a given value, optionally using various
    extensions python-markdown supports.

    Syntax::

        {{ value|markdown2:"extension1_name,extension2_name..." }}

    To enable safe mode, which strips raw HTML and only returns HTML
    generated by actual Markdown syntax, pass "safe" as the first
    extension in the list.

    If the version of Markdown in use does not support extensions,
    they will be silently ignored.

    """
    try:
        import markdown
    except ImportError:
        if settings.DEBUG:
            raise TemplateSyntaxError("Error in content type: The "
                "Markdown library isn't installed.")
        return force_unicode(value)
    else:
        def parse_extra(extra):
            if ':' not in extra:
                return (extra, {})
            name, values = extra.split(':', 1)
            values = dict((str(val.strip()), True) for val in \
                values.split('|'))
            return (name.strip(), values)
        extensions = ['']
        if settings.MARKUP_CODE_HIGHTLIGHT:
            extensions =['codehilite(force_linenos=True)']
        #extras = (e.strip() for e in arg.split(','))
        #extras = dict(parse_extra(e) for e in extras if e)
        #if 'safe' in extras:
        #    del extras['safe']
        #    safe_mode = True
        #else:
        #    safe_mode = False
        return mark_safe(markdown.markdown(force_unicode(value), extensions))

def textile(value):
    """
    parse textile text
    """
    try:
        import textile
    except ImportError:
        if settings.DEBUG:
            raise TemplateSyntaxError("Error in content type: The "
                "Python textile library isn't installed.")
        return force_unicode(value)
    else:
        return mark_safe(force_unicode(textile.textile(smart_str(value), \
            encoding='utf-8', output='utf-8')))


class MarkupContent(models.Model):
    """
    implenment restructured text
    """
    MARKUP_CHOICE = (
        ('rst', 'restructure text'),
        ('markdown', 'markdown'),
        ('textile', 'textile')
    )
    markup = models.TextField(_("Markup Text"), blank=False)
    markup_type = models.CharField(max_length=10, blank=False,
        choices=MARKUP_CHOICE)
    markup_html = models.TextField( blank=False)

    form = MarkupContentAdminForm
    feincms_item_editor_form = MarkupContentAdminForm
    #feincms_item_editor_context_processors = (
    #    lambda x: dict(MARKITUP_JS_URL = settings.MARKITUP_JS_URL),
    #)
    #feincms_item_editor_includes = {
    #    'head': [ 'settings.MARKITUP_CONFIG_URL', ],
    #}

    class Meta:
        abstract = True
        verbose_name = _('Markup')
        verbose_name_plural = _('Markup')

    def save(self, *args, **kwargs):
        self.markup_html = self.parser(self.markup, self.markup_type)
        return super(MarkupContent, self).save(*args, **kwargs)

    def parser(self, value, type=None):
        if type == 'rst':
            convert = restructuredtext(value)
        elif type == 'markdown':
            convert = markdown(value)
        elif type == 'textile':
            convert = textile(value)
        return convert

    def render(self, **kwargs):
        request = kwargs.get('request')
        return render_to_string('content_markup/default.html',
            {'content': self}, context_instance=RequestContext(request))
