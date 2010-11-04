# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class UserProfile(models.Model):
    """
    Define Site Users Profile Base. 3rd Apps can extended it.
    """
    GENDER_CHOICES = (
        (1, 'Male'),
        (2, 'Female'),
    )
    user = models.ForeignKey(User, unique=True)
    realname = models.CharField(max_length=255)
    gender = models.PositiveSmallIntegerField(_('gender'),
        choices=GENDER_CHOICES, blank=True, null=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return u"%s" % self.user.get_full_name()


class ProfileBase(models.Model):
    """
    Root class for extending other custom profile models.
    """
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ['name']
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')

    def save(self, *args, **kwargs):
        pass

    @classmethod
    def register_profile(cls, model, **kwargs):
        pass

    
