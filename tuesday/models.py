from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

# Create your models here.
class Comment(models.Model):
    message = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='writer')
    created_date = models.DateField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, related_name='replies', on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.message


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['message']