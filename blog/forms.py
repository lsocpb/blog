from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordResetForm, \
    SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.forms import ModelForm
from django.forms.widgets import PasswordInput, TextInput
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Invisible, ReCaptchaV2Checkbox
from froala_editor.widgets import FroalaEditor

from blog.models import Post, Tag
from blog.token import token_generator

user_model = get_user_model()


class CommentForm(forms.Form):
    author = forms.CharField(
        max_length=60,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Your Name"
        })
    )
    body = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": "Leave a comment!"
        })
    )


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = user_model
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]

    # We need the user object, so it's an additional parameter
    def send_activation_email(self, request, user):
        current_site = get_current_site(request)
        subject = 'Activate Your Account'
        message = render_to_string(
            'blog/activate_account.html',
            {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token_generator.make_token(user),
            }
        )

        user.email_user(subject, message, html_message=message)


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=TextInput(attrs={
        "class": "form-control",
        "placeholder": "Username"
    }))
    password = forms.CharField(widget=PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Password"
    }))
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible())


class PostForm(ModelForm):
    title = forms.CharField(label='Title',
                            widget=forms.TextInput(
                                attrs={'class': 'w-full focus:ring-0 h-full focus:outline-none text-2xl'}))
    short_description = forms.CharField(label='Short Description',
                                        widget=forms.Textarea(
                                            attrs={'class': 'w-full focus:ring-0 h-full focus:outline-none'}))
    content = forms.CharField(widget=FroalaEditor)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple)
    featured_image_url = forms.CharField(label='Featured Image URL',
                                         widget=forms.TextInput(
                                             attrs={'class': 'w-full focus:ring-0 h-full focus:outline-none'}))

    class Meta:
        model = Post
        fields = ('title', 'short_description', 'content', 'tags', 'visible', 'featured_image_url')


class ProfileForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    date_joined = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control'}))
    password = None

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['date_joined'].widget.attrs['readonly'] = True
        for fieldname in ['username']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ('username', 'email', 'date_joined')


class ResetPasswordForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)

    email = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input",
        "type": "email",
        "placeholder": "Email"
    }))


class NewPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(NewPasswordForm, self).__init__(*args, **kwargs)

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': "input",
            "type": "password",
            'autocomplete': 'new-password'
        }))

    new_password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': "input",
            "type": "password",
            'autocomplete': 'new-password'
        }))
