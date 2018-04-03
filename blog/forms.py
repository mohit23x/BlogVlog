from .models import Comment, CommentReply
from django.forms import ModelForm

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['message']

class CommentReplyForm(ModelForm):
    class Meta:
        model = CommentReply
        fields = ['message']