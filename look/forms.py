from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import *


class PostForm(forms.ModelForm):
    image = forms.ImageField()

    class Meta:
        model = Post
        fields = ['name', 'image', 'description', 'gender']


class CommentForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'comment',
                                                                     'rows': 1, 'cols': 50}))

    class Meta:
        model = Comment
        fields = ['content']


