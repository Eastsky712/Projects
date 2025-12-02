from django.shortcuts import render

from .models import BlogPosts

def index(request):
    """The Home Page for Blogs"""
    return render(request, 'blogs/index.html')
