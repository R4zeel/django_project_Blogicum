from django import forms
from django.forms import ModelForm
from .models import User, Post, Comment


class CreateUserForm(ModelForm):
    model = User


class CreatePostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['author']
        widgets = {
            'text': forms.TextInput(),
            'pub_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local'
            })
        }


class EditPostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['author', 'pub_date']
        widgets = {
            'text': forms.TextInput(),
        }


class AddCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)
        widgets = {
            'comment': forms.TextInput()
        }
