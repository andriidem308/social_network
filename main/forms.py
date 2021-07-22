"""Social Network Forms."""
from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    """Post Form class."""

    body = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': '3',
            'placeholder': 'Share this with the world...'
        }))

    class Meta:
        """Post Form class meta."""

        model = Post
        fields = ['body']
