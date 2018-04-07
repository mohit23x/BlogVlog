from .models import Comment, CommentReply, Blog, Document
from django.forms import ModelForm, ImageField, FileField


class BlogForm(ModelForm):
    class Meta:
        model = Blog
        exclude = ('date', 'star', 'author',)

class DocumentForm(ModelForm):
    image = FileField(label='Image')
    class Meta:
        model = Document
        fields = ('image', )

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['message']

class CommentReplyForm(ModelForm):
    class Meta:
        model = CommentReply
        fields = ['message']