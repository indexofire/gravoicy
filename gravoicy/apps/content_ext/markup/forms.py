# -*- coding: utf-8 -*-
from django import forms
from content_ext.markup.models import MarkupContent

class MarkupForm(forms.ModelForm):
    class Meta:
        model = MarkupContent
        exclude = ('markup_html',)
