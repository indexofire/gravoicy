# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from feincms.module.page.models import Page
from feincms.content.richtext.models import RichTextContent
from feincms.content.image.models import ImageContent
from feincms.content.raw.models import RawContent
from feincms.content.file.models import FileContent
#from feincms.content.rss.models import RSSContent
#from feincms.content.section.models import SectionContent
from content_ext.rst.models import RSTContent


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
            ('sidebar', _('Sidebar'), 'inherited'),
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
)

Page.create_content_type(RichTextContent)
Page.create_content_type(RawContent)
Page.create_content_type(FileContent)
Page.create_content_type(RSTContent)
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
