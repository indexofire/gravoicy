# -*- coding: utf-8 -*-
from django.db import models
from feincms.models import Base
try:
    from mptt.models import MPTTModel
    mptt_register = False
    Base = create_base_model(MPTTModel)
except ImportError:
    mptt_register = True


class Category(Base):
    """
    Contents different levels
    """


class Article(models.Model):
    """
    Contents construct via articles instead of pages.
    """
    PUB_STATUS = (
        ('dra', 'draft'),
        ('del', 'deleted'),
        ('pub', 'published'),
    )

    active = models.BooleanField(_('active'), default=False)

    # structure and navigation
    title = models.CharField(_('title'), max_length=200,
        help_text=_('This is used for the generated navigation too.'))
    slug = models.SlugField(_('slug'), max_length=150)
    parent = models.ForeignKey('self', verbose_name=_('Parent'), blank=True, null=True, related_name='children')
    parent.parent_filter = True # Custom list_filter - see admin/filterspecs.py
    in_navigation = models.BooleanField(_('in navigation'), default=True)
    override_url = models.CharField(_('override URL'), max_length=300, blank=True,
        help_text=_('Override the target URL. Be sure to include slashes at the beginning and at the end if it is a local URL. This affects both the navigation and subpages\' URLs.'))
    redirect_to = models.CharField(_('redirect to'), max_length=300, blank=True,
        help_text=_('Target URL for automatic redirects.'))
    _cached_url = models.CharField(_('Cached URL'), max_length=300, blank=True,
        editable=False, default='', db_index=True)

    request_processors = []
    response_processors = []
    cache_key_components = [ lambda p: django_settings.SITE_ID,
                             lambda p: p._django_content_type.id,
                             lambda p: p.id ]

    class Meta:
        ordering = ['tree_id', 'lft']
        verbose_name = _('page')
        verbose_name_plural = _('pages')



if mptt_register:
    mptt.register(Category)
