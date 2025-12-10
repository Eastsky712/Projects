from django.db import models

class Topic(models.Model):
    """A Topic the user wants there post to be about"""
    text = models.CharField(max_length=50)

    def __str__(self):
        """Return a string represetation of the model."""
        return self.text
    
class Post(models.Model):
    """A blog post of the choosen topic"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=30)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'posts'

    def __str__(self):
        """Return a string representation of the model"""
        return f"{self.subject}"