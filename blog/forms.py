from .models import Comment, CommentReply, Blog, Document, UserImage, UserInfo
from django.forms import ModelForm, ImageField, FileField
from PIL import Image
from django import forms
from django.core.files.images import get_image_dimensions
from django.core.files import File
from simple_search import search_form_factory


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


class UserImageForm(ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = UserImage
        fields = ('myimage','x', 'y', 'width', 'height')


    def save(self):
        photo = super(UserImageForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.myimage)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(photo.myimage.path)

        return photo

class UserInfoForm(ModelForm):
    email = forms.EmailField()
    class Meta:
        model = UserInfo
        exclude = ('author', 'views')
        fields = ('displayname', 'designation', 'description', 'birthdate', 'email')
#        fields = '__all__'


