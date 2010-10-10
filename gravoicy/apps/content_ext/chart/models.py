# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string


class Chart(models.Model):
    """
    Base Chart Class
    """

    class Meta:
        abstract = True


class HighCharts(models.Model):
    """
    HighCharts Class
    """
    CHARTS_TYPE = (
        ('line', 'line'),
        ('scatter', 'scatter'),
        ('spline', 'spine'),
        ('area', 'area'),
        ('areaspline', 'areaspline'),
        ('bar', 'bar'),
        ('column', 'column'),
    )
    height = models.PositiveIntegerField(default=400)
    width = models.PositiveIntegerField(default=480)
    type = models.CharField(max_length=20, choices=CHARTS_TYPE)
    data = models.TextField()
    title = models.CharField(max_length=255, blank=True)
    subtitle = models.CharField(max_length=255, blank=True)
    x = models.TextField(blank=True)
    y = models.TextField(blank=True)
    tooltip = models.TextField(blank=True)
    plot_options = models.TextField(blank=True)
    #other = models.TextField(blank=True)

    class Meta:
        abstract = True

    def parse(self):
        pass

    def render(self, **kwargs):
        request = kwargs.get('request')
        content = "chart:{renderTo: 'chart', defaultSeriesType: '%s'},\n" % self.type
        content += "xAxis:{%s},\n" % self.x
        content += "yAxis:{%s},\n" % self.y
        content += "tooltip:{%s},\n" % self.tooltip
        content += "plotOptions:{%s},\n" % self.plot_options
        content += "series:[%s],\n" % self.data
        content += "title:{text:'%s'},\n" % self.title
        content += "subtitle:{text:'%s'},\n" % self.subtitle
        return render_to_string('content_ext/chart/default.html',
            {'content': mark_safe(content), 'request': request})
