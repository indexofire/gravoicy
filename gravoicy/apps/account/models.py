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
    realname = models.CharField(
    gender = models.PositiveSmallIntegerField(_('gender'),
        choices=GENDER_CHOICES, blank=True, null=True)
    
    class Meta:
        abstract = True

    def __unicode__(self):
        return u"%s" self.user.get_full_name
