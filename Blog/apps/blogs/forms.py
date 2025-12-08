from django import forms

from .models import BlogTitle, BlogPost

class TitleForm(forms.ModelForm):
    class Meta:
        model = BlogTitle
        fields = ['title']
        labels = {'title': ''}

class PostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['post']
        labels = {'post':''}
        widgets = {'post': forms.Textarea(attrs={'cols': 80})}
