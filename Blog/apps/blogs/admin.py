from django.contrib import admin

from .models import BlogPost, BlogTitle

admin.site.register(BlogTitle)
admin.site.register(BlogPost)

