from django.urls import path
from . import views

app_name = 'blogs'
urlpatterns = [
    # Home Page
    path('', views.index, name='index'),
    # Page which shows all Blog Posts
    path('titles/', views.titles, name='titles'),
    # Page which shows one Blog Post
    path('titles/<int:post_id>/', views.title, name='title'),
    # Page which makes a new post
    path('new_post/', views.new_post, name='new_post'),
]