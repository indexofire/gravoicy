# -*- coding: utf-8 -*-
from django.contrib import admin
from article.models import Article
from article.forms import ArticleAdminForm
from feincms.admin.editor import ItemEditor, TreeEditor


class ArticleAdmin(ItemEditor, TreeEditor):
    """
    Article Control Panel in Admin
    """
    class Media:
        css = {}
        js = []

    form = ArticleAdminForm

    # the fieldsets config here is used for the add_view, it has no effect
    # for the change_view which is completely customized anyway
    unknown_fields = ['override_url', 'redirect_to']
    fieldsets = [
        (None, {
            'fields': ['active', 'in_navigation', 'template_key', 'title', 'slug',
                'parent'],
        }),
        item_editor.FEINCMS_CONTENT_FIELDSET,
        (_('Other options'), {
            'classes': ['collapse',],
            'fields': unknown_fields,
        }),
        ]
    readonly_fields = []
    list_display = ['short_title', 'is_visible_admin', 'in_navigation_toggle', 'template']
    list_filter = ['active', 'in_navigation', 'template_key', 'parent']
    search_fields = ['title', 'slug']
    prepopulated_fields = { 'slug': ('title',), }

    raw_id_fields = ['parent']
    radio_fields = {'template_key': admin.HORIZONTAL}

    def __init__(self, *args, **kwargs):
        ensure_completely_loaded()

        if len(Article._feincms_templates) > 4:
            del(self.radio_fields['template_key'])

        super(ArticleAdmin, self).__init__(*args, **kwargs)

        # The use of fieldsets makes only fields explicitly listed in there
        # actually appear in the admin form. However, extensions should not be
        # aware that there is a fieldsets structure and even less modify it;
        # we therefore enumerate all of the model's field and forcibly add them
        # to the last section in the admin. That way, nobody is left behind.
        from django.contrib.admin.util import flatten_fieldsets
        present_fields = flatten_fieldsets(self.fieldsets)

        for f in self.model._meta.fields:
            if not f.name.startswith('_') and not f.name in ('id', 'lft', 'rght', 'tree_id', 'level') and \
                    not f.auto_created and not f.name in present_fields and f.editable:
                self.unknown_fields.append(f.name)
                if not f.editable:
                    self.readonly_fields.append(f.name)

    in_navigation_toggle = editor.ajax_editable_boolean('in_navigation', _('in navigation'))

    def _actions_column(self, page):
        actions = super(PageAdmin, self)._actions_column(page)
        actions.insert(0, u'<a href="add/?parent=%s" title="%s"><img src="%simg/admin/icon_addlink.gif" alt="%s"></a>' % (
            page.pk, _('Add child page'), django_settings.ADMIN_MEDIA_PREFIX ,_('Add child page')))
        actions.insert(0, u'<a href="%s" title="%s"><img src="%simg/admin/selector-search.gif" alt="%s" /></a>' % (
            page.get_absolute_url(), _('View on site'), django_settings.ADMIN_MEDIA_PREFIX, _('View on site')))
        return actions

    def add_view(self, request, form_url='', extra_context=None):
        # Preserve GET parameters
        return super(PageAdmin, self).add_view(
            request=request,
            form_url=request.get_full_path(),
            extra_context=extra_context)

    def response_add(self, request, obj, *args, **kwargs):
        response = super(PageAdmin, self).response_add(request, obj, *args, **kwargs)
        if 'parent' in request.GET and '_addanother' in request.POST and response.status_code in (301, 302):
            # Preserve GET parameters if we are about to add another page
            response['Location'] += '?parent=%s' % request.GET['parent']
        if 'translation_of' in request.GET:
            # Copy all contents
            try:
                original = self.model._tree_manager.get(pk=request.GET.get('translation_of'))
                original = original.original_translation
                obj.copy_content_from(original)
                obj.save()
            except self.model.DoesNotExist:
                pass

        return response

    def _refresh_changelist_caches(self, *args, **kwargs):
        self._visible_pages = list(self.model.objects.active().values_list('id', flat=True))

    def change_view(self, request, object_id, extra_context=None):
        from django.shortcuts import get_object_or_404
        if 'create_copy' in request.GET:
            page = get_object_or_404(Page, pk=object_id)
            new = Page.objects.create_copy(page)
            self.message_user(request, ugettext("You may edit the copied page below."))
            return HttpResponseRedirect('../%s/' % new.pk)
        elif 'replace' in request.GET:
            page = get_object_or_404(Page, pk=request.GET.get('replace'))
            with_page = get_object_or_404(Page, pk=object_id)
            Page.objects.replace(page, with_page)
            self.message_user(request, ugettext("You have replaced %s. You may continue editing the now-active page below.") % page)
            return HttpResponseRedirect('.')

        # Hack around a Django bug: raw_id_fields aren't validated correctly for
        # ForeignKeys in 1.1: http://code.djangoproject.com/ticket/8746 details
        # the problem - it was fixed for MultipleChoiceFields but not ModelChoiceField
        # See http://code.djangoproject.com/ticket/9209

        if hasattr(self, "raw_id_fields"):
            for k in self.raw_id_fields:
                if not k in request.POST:
                    continue
                if not isinstance(getattr(Page, k).field, models.ForeignKey):
                    continue

                v = request.POST[k]

                if not v:
                    del request.POST[k]
                    continue

                try:
                    request.POST[k] = int(v)
                except ValueError:
                    request.POST[k] = None

        return super(PageAdmin, self).change_view(request, object_id, extra_context)

    def render_item_editor(self, request, object, context):
        if object:
            try:
                active = Page.objects.active().exclude(pk=object.pk).get(_cached_url=object._cached_url)
                context['to_replace'] = active
            except Page.DoesNotExist:
                pass

        return super(PageAdmin, self).render_item_editor(request, object, context)

    def is_visible_admin(self, page):
        """
        Instead of just showing an on/off boolean, also indicate whether this
        page is not visible because of publishing dates or inherited status.
        """
        if not hasattr(self, "_visible_pages"):
            self._visible_pages = list() # Sanity check in case this is not already defined

        if page.parent_id and not page.parent_id in self._visible_pages:
            # parent page's invisibility is inherited
            if page.id in self._visible_pages:
                self._visible_pages.remove(page.id)
            return editor.ajax_editable_boolean_cell(page, 'active', override=False, text=_('inherited'))

        if page.active and not page.id in self._visible_pages:
            # is active but should not be shown, so visibility limited by extension: show a "not active"
            return editor.ajax_editable_boolean_cell(page, 'active', override=False, text=_('extensions'))

        return editor.ajax_editable_boolean_cell(page, 'active')
    is_visible_admin.allow_tags = True
    is_visible_admin.short_description = _('is active')
    is_visible_admin.editable_boolean_field = 'active'

    # active toggle needs more sophisticated result function
    def is_visible_recursive(self, page):
        retval = []
        for c in page.get_descendants(include_self=True):
            retval.append(self.is_visible_admin(c))
        return retval
    is_visible_admin.editable_boolean_result = is_visible_recursive
admin.site.register(Article, ArticleAdmin)
