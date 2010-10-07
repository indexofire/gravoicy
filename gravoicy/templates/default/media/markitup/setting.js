django.jQuery(document).ready(function() {
    django.jQuery("select[name^='markupcontent_set-']").change(function() {
        var id = django.jQuery(this).attr('id').replace('id_markupcontent_set-', '').replace('-markup_type','');
        var type = django.jQuery(this).val();
        var attr = 'textarea#id_markupcontent_set-' + id + '-markup';
        django.jQuery(attr).markItUpRemove();
        switch(type) {
            case 'textile':
                django.jQuery(attr).markItUp(myTextileSettings);
                break;
            case 'markdown':
                django.jQuery(attr).markItUp(myMarkdownSettings);
                break;
            case 'rst':
                django.jQuery(attr).markItUp(myRestructuredTextSettings);
        }
        return false;
    });
});
