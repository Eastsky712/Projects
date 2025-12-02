from django.db import models

class BlogPosts(models.Model):
    """A Post where user can write down their blogs"""
    title = models.CharField(max_length=50)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string represetation of the model."""
        return self.title