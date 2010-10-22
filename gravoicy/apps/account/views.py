# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from account.models import UserProfile
#from forms import SignatureForm


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
def profile_create(request, username, template_name="account/profile_create.html"):
    pass

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
    user = get_object_or_404(UserProfile, username=username)
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
