# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from account.models import UserProfile


class SignatureForm(forms.Form):
    # name =  forms.CharField(label = 'Name', max_length=50)
    email = forms.EmailField(label = 'Email Address', help_text = 'Required')
    content = forms.CharField(widget = forms.widgets.Textarea(attrs = {
        'rows' : 4,
        'style' : 'width:100%;',
        'cols' : 20
        }),
        label = 'Comments', help_text = 'Optional', required = False
    )

    def clean_content(self):
      data = self.clean_data['content']
      if "http://" in data:
          raise forms.ValidationError("Cannot have HTML/Links in the comment")

      return data

@login_required
def profile_create(request, username,
    template_name="account/profile_create.html"):
    """
    Create a profile for the current user, if one doesn't already
    exist.

    If the user already has a profile, as determined by
    'request.user.get_profile()', a redirect will be issued to the
    :view: profiles.views.edit_profile view. If no profile model has
    been specified in the ``AUTH_PROFILE_MODULE`` setting,
    'django.contrib.auth.models.SiteProfileNotAvailable' will be
    raised.

    **Optional arguments:**

    extra_context
        A dictionary of variables to add to the template context. Any
        callable object in this dictionary will be called to produce
        the end result which appears in the context.

    form_class
        The form class to use for validating and creating the user
        profile. This form class must define a method named
        ``save()``, implementing the same argument signature as the
        ``save()`` method of a standard Django ``ModelForm`` (this
        view will call ``save(commit=False)`` to obtain the profile
        object, and fill in the user before the final save). If the
        profile object includes many-to-many relations, the convention
        established by ``ModelForm`` of using a method named
        ``save_m2m()`` will be used, and so your form class should
        also define this method.

        If this argument is not supplied, this view will use a
        ``ModelForm`` automatically generated from the model specified
        by ``AUTH_PROFILE_MODULE``.

    success_url
        The URL to redirect to after successful profile creation. If
        this argument is not supplied, this will default to the URL of
        :view:`profiles.views.profile_detail` for the newly-created
        profile object.

    template_name
        The template to use when displaying the profile-creation
        form. If not supplied, this will default to
        :template:`profiles/create_profile.html`.

    **Context:**

    form
        The profile-creation form.

    **Template:**

    template_name keyword argument, or
    :template: profiles/create_profile.html.

    """
    try:
        profile_obj = request.user.get_profile()
        return HttpResponseRedirect(reverse('profile-edit'))
    except ObjectDoesNotExist:
        pass

    # We set up success_url here, rather than as the default value for
    # the argument. Trying to do it as the argument's default would
    # mean evaluating the call to reverse() at the time this module is
    # first imported, which introduces a circular dependency: to
    # perform the reverse lookup we need access to profiles/urls.py,
    # but profiles/urls.py in turn imports this module.

    if success_url is None:
        success_url = reverse('profile-detail',
            kwargs={'username': request.user.username})

    if form_class is None:
        form_class = utils.get_profile_form()

    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            profile_obj = form.save(commit=False)
            profile_obj.user = request.user
            profile_obj.save()
            if hasattr(form, 'save_m2m'):
                form.save_m2m()
            return HttpResponseRedirect(success_url)
    else:
        form = form_class()

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response(template_name,
        {'form': form,},
        context_instance=context,)

@login_required
def profile_detail(request, username, is_public=True, extra_context=None,
    template_name="account/profile_detail.html"):
    """
    Detail view of a user's profile.

    If no profile model has been specified in the 'AUTH_PROFILE_MODULE'
    setting, 'django.contrib.auth.models.SiteProfileNotAvailable' will be
    raised.

    If the user has not yet created a profile, 'Http404' will be raised.

    **Required arguments:**

    username
        The username of the user whose profile is being displayed.

    **Optional arguments:**

    extra_context
        A dictionary of variables to add to the template context. Any
        callable object in this dictionary will be called to produce
        the end result which appears in the context.

    is_public
        The name of a 'BooleanField' on the profile model; if the
        value of that field on the user's profile is 'False', the
        'profile' variable in the template will be 'Non'. Use
        this feature to allow users to mark their profiles as not
        being publicly viewable.

        If this argument is not specified, it will be assumed that all
        users' profiles are publicly viewable.

    template_name
        The name of the template to use for displaying the profile. If
        not specified, this will default to
        :template:`profiles/profile_detail.html`.

    **Context:**

    profile
        The user's profile, or 'None' if the user's profile is not
        publicly viewable (see the description of 'is_public' above).

    **Template:**

    template_name
        keyword argument or 'account/profile_detail.html'.
    """
    user = get_object_or_404(User, username=username)
    try:
        profile_obj = user.get_profile()
    except ObjectDoesNotExist:
        raise Http404

    context = {
        'profile': profile_obj,
    }

    if extra_context is None:
        extra_context = {}
    for k, v in extra_context.items():
        context[k] = callable(v) and v() or v

    return render_to_response(template_name, context, RequestContext(request))

@login_required
def signature(request, form_class=SignatureForm, template_name="account/signature.html"):
    profile = request.user.lbforum_profile
    if request.method == "POST":
        form = form_class(instance=profile, data=request.POST)
        form.save()
    else:
        form = form_class(instance=profile)
    ext_ctx = {'form': form}
    return render_to_response(template_name, ext_ctx, RequestContext(request))

"""
def create(request, template_name='accounts/create.html',
    redirect_field_name='redirect_to'):

    user_form = None
    captcha_error = ""
    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        captcha_response = captcha.submit(
            request.POST.get("recaptcha_challenge_field", None),
            request.POST.get("recaptcha_response_field", None),
            settings.RECAPTCHA_PRIVATE_KEY,
            request.META.get("REMOTE_ADDR", None))

        if not captcha_response.is_valid:
            captcha_error = "&error=%s" % captcha_response.error_code
        else:
            # perform other registration checks as needed...
            # success!
            return HttpResponseRedirect(redirect_to)

    if not user_form:
        user_form = UserForm(prefix="user")

    return render_to_response(template_name, {
        'captcha_error': captcha_error,
        'user_form': user_form},
        context_instance=RequestContext(request))
"""

@login_required
def profile_edit(request, template_name="account/profile_edit.html"):
    pass
