from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from froala_editor.widgets import FroalaEditor

from blog.models import Post, Tag
from django.forms import ModelForm


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


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "password1", "password2"]


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
        fields = ('title', 'short_description', 'content', 'tags', 'visible')

