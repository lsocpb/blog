from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.forms.widgets import PasswordInput, TextInput
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from froala_editor.widgets import FroalaEditor

from blog.models import Post, Tag
from django.forms import ModelForm

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
    username = forms.CharField(widget=TextInput(attrs={
        "class": "form-control",
        "placeholder": "Username"
    }))
    password = forms.CharField(widget=PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Password"
    }))


class PostForm(ModelForm):
    title = forms.CharField(label='Title',
                            widget=forms.TextInput(
                                attrs={'class': 'w-full focus:ring-0 h-full focus:outline-none text-2xl'}))
    content = forms.CharField(widget=FroalaEditor)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Post
        fields = ('title', 'short_description', 'content', 'tags', 'visible', 'featured_image')

