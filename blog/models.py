from django.db import models
from django.urls import reverse

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=250, null=True, blank=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('postdetail', args=[str(self.id)])


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    message = models.CharField(max_length = 250)

    def __str__(self):
        return self.message

class CommentReply(models.Model):
    whichcomment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    message = models.CharField(max_length = 250)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.message

