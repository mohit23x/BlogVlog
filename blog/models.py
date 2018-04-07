from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
import os

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200, null=True, blank=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()
    date = models.DateField(auto_now_add=True, blank=True, null=True)
    #document = models.FileField(upload_to='documents/', blank=True, null=True)
    star = models.PositiveIntegerField(default=0)
    topbanner =  models.FileField(upload_to='documents/banner/', blank=True, null=True, default='documents/03.jpg')
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('postdetail', args=[str(self.id)])


def get_image_filename(instance, filename):
    title = instance.blog.id
    slug = slugify(title)
    return "post_images_{}/{}".format(slug, filename)


class Document(models.Model):
    blog = models.ForeignKey(Blog, default=None, on_delete=models.CASCADE)
    image = models.FileField(upload_to=get_image_filename, verbose_name = 'Image')

    def filename(self):
        return os.path.basename(self.image.name)


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

