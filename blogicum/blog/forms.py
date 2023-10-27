from django import forms
from django.forms import ModelForm

from .models import Post, Comment


class CreatePostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['author']
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local'
            })
        }


class AddCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
