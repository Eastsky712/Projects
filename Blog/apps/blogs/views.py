from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Topic, Post
from .forms import TopicForm, PostForm

def index(request):
    """The Home Page for Blogs"""
    return render(request, 'blogs/index.html')

@login_required
def topics(request):
    """The Blog Posts Page"""
    topics = Topic.objects.order_by('text')
    context = {'topics': topics}
    return render(request, 'blogs/topics.html', context)

def topic(request, topic_id):
    """Shows a single Blog Post and its contents"""
    topic = Topic.objects.get(id=topic_id)
    posts = topic.post_set.order_by('-date_added')
    context = {'topic': topic, 'posts': posts}
    return render(request, 'blogs/topic.html', context)

def new_post(request, topic_id):
    """Adds new Post"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = PostForm()
    else:
        # POST data submitted; process data.
        form = PostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.topic = topic
            new_post.save()
            return redirect('blogs:topic', topic_id=topic_id)
    
    # Display a blank or invalid form.
    context = {'topic': topic, 'form': form}
    return render(request, 'blogs/new_post.html', context)

def new_topic(request):
    """Add a new title"""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:topics')
        
    # Display a blank or invalid form
    context = {'form': form}
    return render(request, 'blogs/new_topic.html', context)

def edit_post(request, post_id):
    """Edit a existing post"""
    post = Post.objects.get(id=post_id)
    topic = post.topic
    author = post.author

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = PostForm(instance=post)
    else:
        # POST data submitted; process data.
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:topic', topic_id=topic.id)
    
    context = {'post': post, 'topic': topic, 'form': form}
    return render(request, 'blogs/edit_post.html', context)

def delete_post(request, post_id, topic_id):
    """Delete a existing post"""
    post = Post.objects.get(id=post_id)
    topic = Topic.objects.get(id=topic_id)

    context = {'post': post, 'topic': topic} 
    return render(request, 'blogs/delete_post.html', context)
