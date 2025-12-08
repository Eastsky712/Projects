from django.shortcuts import render, redirect

from .models import BlogTitle, BlogPost
from .forms import PostForm

def index(request):
    """The Home Page for Blogs"""
    return render(request, 'blogs/index.html')

def titles(request):
    """The Blog Posts Page"""
    posts = BlogTitle.objects.order_by('date_added')
    context = {'titles': posts}
    return render(request, 'blogs/titles.html', context)

def title(request, post_id):
    """Shows a single Blog Post and its contents"""
    post = BlogTitle.objects.get(id=post_id)
    context = {'title': post}
    return render(request, 'blogs/title.html', context)

def new_post(request, title_id):
    """Adds new Post"""
    title = BlogPost.objects.get(id=title_id)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = PostForm()
    else:
        # POST data submitted; process data.
        form = PostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.title = title
            new_post.save()
            return redirect('blogs:titles', titles_id=title_id)
    
    # Display a blank or invalid form.
    context = {'title': title, 'form': form}
    return render(request, 'blogs/new_post.html', context)