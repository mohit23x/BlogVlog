from django.urls import path
from . import views
from django.contrib.auth.urls import views as auth_views
from django.conf.urls import url

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('password_reset', auth_views.password_reset, name='password_reset'),
    path('password_reset_done', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    path('password_reset_complete', auth_views.password_reset_complete, name='password_reset_complete'),

]