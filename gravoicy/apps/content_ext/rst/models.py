# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_str, force_unicode
from docutils.core import publish_parts
from docutils.parsers.rst import directives, Directive
from content_ext.rst.directives.code import CodeHighlight
from feincms.module.page.models import Page


class RSTContent(models.Model):
    """
    implenment restructured text
    """
    rst = models.TextField(_("content"), blank=True)
    rst_html = models.TextField(editable=False, blank=True)

    class Meta:
        abstract = True
        verbose_name = _('Restructured Text')
        verbose_name_plural = _('Restructured Texts')

    def save(self, *args, **kwargs):
        self.rst_html = self.parser(self.rst)
        return super(RSTContent, self).save(*args, **kwargs)

    def parser(self, value):
        docutils_settings = getattr(settings,
            'RESTRUCTUREDTEXT_FILTER_SETTINGS', {},)
        directives.register_directive('code', CodeHighlight)
        parts = publish_parts(source=smart_str(value),
            writer_name="html4css1",
            settings_overrides=docutils_settings,)
        return force_unicode(parts["html_body"])

    def render(self, **kwargs):
        return self.rst_html
