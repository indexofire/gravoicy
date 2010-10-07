# -*- coding: utf-8 -*-
from django.conf import settings
from django.forms import Textarea
from django.forms.util import flatatt
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode


class MarkItUpWidget(Textarea):
    """
    MarkItUp Widget class
    """
    class Media:
        js = (
            'markitup/jquery.markitup.js',
            'markitup/sets/restructuredtext/set.js',
            'markitup/sets/textile/set.js',
            'markitup/sets/markdown/set.js',
            'markitup/setting.js',
        )
        css = {
            'all': (
                'markitup/skins/simple/style.css',
                'markitup/sets/restructuredtext/style.css',
                'markitup/sets/textile/style.css',
                'markitup/sets/markdown/style.css',
            )
        }

    def __init__(self, type=None, attrs=None):
        default_attrs = {'cols': '40', 'rows': '10'}
        if attrs:
            default_attrs.update(attrs)
        super(Textarea, self).__init__(default_attrs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        insert = '''<ul class="switcher">
            <li class="restructuredtext"><a href="#">Restructured Text</a></li>
            <li class="textile"><a href="#">Textile</a></li>
            <li class="markdown"><a href="#">MarkDown</a></li>
            </ul>'''
        return mark_safe(u'%s<textarea class="multiSet" %s>%s</textarea>'
            % (insert, flatatt(final_attrs), conditional_escape(force_unicode(value))))


#class AdminMarkItUpWidget(MarkItUpWidget, AdminTextareaWidget):
#    """
#    Add LargeTextarea class to MarkItUpWidget so it looks more similar to
#    other admin textareas.
#    """
#    pass
