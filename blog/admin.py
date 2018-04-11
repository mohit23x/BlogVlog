from django.contrib import admin
from .models import Blog, Comment, CommentReply, Document, UserImage, UserInfo, Hashtag
# Register your models here.

admin.site.register(Blog)
admin.site.register(Document)
admin.site.register(Comment)
admin.site.register(CommentReply)
admin.site.register(UserImage)
admin.site.register(UserInfo)
admin.site.register(Hashtag)