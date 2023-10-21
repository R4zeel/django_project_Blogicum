from django import forms
from django.forms import ModelForm
from .models import User, Post


class CreateUserForm(ModelForm):
    model = User


class CreatePostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['pub_date', 'author']
        widgets = {
            'text': forms.TextInput()
        }
