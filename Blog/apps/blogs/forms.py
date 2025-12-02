from django import forms

from .models import BlogPosts

class BlogForms(forms.ModelForm):
    class Meta:
        model = BlogPosts
        fields = ['text']
        labels = {'text':''}