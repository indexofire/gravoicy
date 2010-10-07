django.jQuery(document).ready(function() {
    django.jQuery('.multiSet').markItUp(myRestructuredTextSettings);

    django.jQuery('.switcher li').click(function() {
            django.jQuery('.multiSet').markItUpRemove();
            newSet = $(this).attr('class');
            switch(newSet) {
                case 'textile':
                    django.jQuery('.multiSet').markItUp(myTextileSettings);
                    break;
                case 'markdown':
                    django.jQuery('.multiSet').markItUp(myMarkdownSettings);
                    break;
                case 'restructuredtext':
                    django.jQuery('.multiSet').markItUp(myRestructuredTextSettings);
            }
            return false;
        }
    );
});
