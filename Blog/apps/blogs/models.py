from django.db import models

class BlogTitle(models.Model):
    """A title the user wants there blog to be about"""
    title = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string represetation of the model."""
        return self.title
    
class BlogPost(models.Model):
    """A blog post of the title"""
    title = models.ForeignKey(BlogTitle, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'posts'

    def __str__(self):
        """Return a string representation of the model"""
        return f"{self.post[:50]}..."