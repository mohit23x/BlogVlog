from django.urls import path, include
from blog import urls
from . import views

urlpatterns = [
    path('', views.Homepage.as_view(), name='homepage'),
    path('aboutus', views.AboutUs.as_view(), name="aboutus"),
    path('post/<int:pk>', views.PostDetail, name='postdetail'),
    path('newpost', views.newpost, name='newpost'),
    path('usrinfo', views.user_image_func, name='usrinfo'),
    path('postedit/<int:pk>', views.PostEdit.as_view(), name='postedit'),
    path('postdelete/<int:pk>', views.BlogDelete.as_view(), name='postdelete'),
    path('mypost/<author>', views.MyPost.as_view(), name='myposts'),
    path('commentreplydelete/<int:pk>', views.CommentReplyDelete.as_view(), name='commentreplydelete'),
    path('commentdelete/<int:pk>', views.CommentDelete.as_view(), name='commentdelete'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('post/postnew', views.BlogPostNew.as_view(), name='postnew'),
    path('profile/<str:nam>', views.profile, name='profile'),
    path('editprofileinfo/<int:pk>', views.userInfoFormView, name='editprofileinfo'),
    path('search', views.search, name='search'),
    path('category/<str:hashtags>', views.categoryview, name='category'),

]