# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string


class GoogleMaps(models.Model):
    """
    Google Maps v3
    """
    title = models.CharField(_("map title"), max_length=100, blank=True,
        null=True, default="Google Maps")
    address = models.CharField(_("address"), max_length=150, blank=True,
        null=True, default="Hangzhou")
    zipcode = models.CharField(_("zip code"), max_length=30, blank=True,
        null=True, default="310000")
    city = models.CharField(_("city"), max_length=100, blank=True, null=True,
        default="Hangzhou")
    content = models.CharField(_("additional content"), max_length=255,
        blank=True, null=True, default="Map Content")
    zoom = models.IntegerField(_("zoom level"), blank=True, null=True,
        default=13)
    lat = models.DecimalField(_('latitude'), max_digits=10, decimal_places=6,
        null=True, blank=True, 
        help_text=_('use latitude to define the map possiton'))
    lng = models.DecimalField(_('longitude'), max_digits=10, decimal_places=6,
        null=True, blank=True,
        help_text=_('use longitude to define the map possiton'),)
    route_planer_title = models.CharField(_("route planer title"),
        max_length=150, blank=True, null=True,
        help_text=_("calculate your fastest way to here"))
    route_planer = models.BooleanField(_("route planer"), default=False)

    class Meta:
        abstract = True

    def get_lat_lng(self):
        if self.lat and self.lng:
            return [self.lat, self.lng]

    def render(self, **kwargs):
        return render_to_string('googlemap/default.html',
            {'object': self,},
        )
