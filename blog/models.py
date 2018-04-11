from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
import os
from PIL import Image

# Create your models here.

class Hashtag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


def get_topbanner_filename(instance, filename):
    title = instance.title
    slug = slugify(title)
    return "documents/banner/{}/{}".format(slug, filename)

class Blog(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200, null=True, blank=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()
    date = models.DateField(auto_now_add=True, blank=True, null=True)
    star = models.PositiveIntegerField(default=0)
    topbanner =  models.ImageField(upload_to=get_topbanner_filename, null=True, blank=True)
    category  = models.ForeignKey(Hashtag,  on_delete=models.CASCADE, null=True, blank=True)
    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('postdetail', args=[str(self.id)])

#, default='documents/03.jpg'


def get_image_filename(instance, filename):
    title = instance.blog.id
    slug = slugify(title)
    return "post_images/post_images_{}/{}".format(slug, filename)


class Document(models.Model):
    blog = models.ForeignKey(Blog, default=None, on_delete=models.CASCADE)
    image = models.FileField(upload_to=get_image_filename, verbose_name = 'Image')

    def filename(self):
        return os.path.basename(self.image.name)

#-----------------------------------------------------------

def get_user_image_filename(instance, filename):
    title = instance.author
    slug = slugify(title)
    return "user_image_{}/{}".format(slug, filename)

class UserImage(models.Model):
    author = models.OneToOneField('auth.User', on_delete=models.CASCADE, null=True, default=True)
    myimage = models.ImageField(upload_to=get_user_image_filename, default='user_image_noimg/jobs.jpg', null=True, blank=True)


#------------------------------------------------------

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    message = models.CharField(max_length = 250)
    usrimg = models.ForeignKey(UserImage, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.message


class CommentReply(models.Model):
    whichcomment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    message = models.CharField(max_length = 250)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    usrimg = models.ForeignKey(UserImage, on_delete=models.CASCADE, null=True, blank=True)

    

    def __str__(self):
        return self.message





#------------------------------------------------------

class UserInfo(models.Model):
    author = models.OneToOneField('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    displayname = models.CharField(max_length=50, null=True, blank=True)
    designation = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=250, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    views = models.PositiveIntegerField(default = 0)

    def get_absolute_url(self):
        return reverse('homepage')

#-------------------------------------------------------