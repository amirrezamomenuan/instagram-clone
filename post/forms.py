from django import forms
from .models import Post, Comment, Like, Reply

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption', 'location']