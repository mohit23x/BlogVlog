from django.urls import path, include
from blog import urls
from . import views

urlpatterns = [
    path('', views.Homepage.as_view(), name='homepage'),
    path('post/<int:pk>', views.PostDetail, name='postdetail'),
    path('postedit/<int:pk>', views.PostEdit.as_view(), name='postedit'),
    path('postdelete/<int:pk>', views.BlogDelete.as_view(), name='postdelete'),
    path('mypost/<author>', views.MyPost.as_view(), name='myposts'),
    path('commentreplydelete/<int:pk>', views.CommentReplyDelete.as_view(), name='commentreplydelete'),
    path('commentdelete/<int:pk>', views.CommentDelete.as_view(), name='commentdelete'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('post/postnew', views.BlogPostNew.as_view(), name='postnew')
]