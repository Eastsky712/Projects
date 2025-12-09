from django.urls import path
from . import views

app_name = 'blogs'
urlpatterns = [
    # Home Page
    path('', views.index, name='index'),
    # Page which shows all Blog Posts
    path('topics/', views.topics, name='topics'),
    # Page which shows one Blog Post
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    # Page which makes a new post topic
    path('new_topic/', views.new_topic, name='new_topic'),
    # Page which makes a new post comment
    path('new_post/<int:topic_id>/', views.new_post, name='new_post'),
    # Page where you can edit a existing post
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    # This page will be used to delete a existing post
    path('edit_post/<int:post_id>/delete_post', views.delete_post, name='delete_post'),
]