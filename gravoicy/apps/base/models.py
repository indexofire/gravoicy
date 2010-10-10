# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from feincms.module.page.models import Page
from feincms.content.application.models import ApplicationContent
from feincms.content.richtext.models import RichTextContent
from feincms.content.image.models import ImageContent
from feincms.content.raw.models import RawContent
from feincms.content.file.models import FileContent
#from feincms.content.contactform.models import ContactForm
#from feincms.content.rss.models import RSSContent
#from feincms.content.section.models import SectionContent
from content_ext.markup.models import MarkupContent
from content_ext.chart.models import HighCharts


# Example set of extensions
Page.register_extensions(
    'datepublisher',
    'changedate',
    'translations',
    'navigation',
    'seo',
    'symlinks',
    'titles',
)

Page.register_templates(
    {
        'title': _('Standard Template'),
        'path': 'base.html',
        'regions': (
            ('main', _('Main content area')),
            ('sidebar', _('Sidebar'), 'inherited'),
        ),
    },
    {
        'title': _('Two Columns Page'),
        'path': 'col_two.html',
        'regions': (
            ('main', _('Main content area')),
            ('right', _('Right'), 'inherited'),
        ),
    },
    {
        'title': _('Three Columns Page'),
        'path': 'col_three.html',
        'regions': (
            ('main', _('Main content area')),
            ('sidebar', _('Sidebar'), 'inherited'),
            ('right', _('Right')),
        ),
    },
    {
        'title': _('Forum Page'),
        'path': 'forum.html',
        'regions': (
            ('main', _('Main content area')),
        ),
    },
)

Page.create_content_type(RichTextContent)
Page.create_content_type(RawContent)
Page.create_content_type(FileContent)
Page.create_content_type(MarkupContent)
Page.create_content_type(HighCharts)
#Page.create_content_type(ContactForm)
#Page.create_content_type(RSSContent)
#Page.create_content_type(SectionContent)
Page.create_content_type(
    ImageContent,
    POSITION_CHOICES=(
        ('block', _('block')),
        ('left', _('left')),
        ('right', _('right')),
    )
)


if 'forum' in settings.INSTALLED_APPS:
    Page.create_content_type(ApplicationContent, APPLICATIONS=(
        ('forum.urls', 'Forum Application'),)
    )
