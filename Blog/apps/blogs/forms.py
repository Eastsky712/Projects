from django import forms

from .models import Topic, Post

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','author','text']
        labels = {'text':''}
        widgets = {
            'text': forms.Textarea(attrs={'cols': 80, 'form': 'edit-form'}), 
            'author': forms.TextInput(attrs={'form': 'edit-form'}), 
            'title': forms.TextInput(attrs={'form': 'edit-form'}) 
            }

