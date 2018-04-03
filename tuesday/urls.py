from django.urls import path, include

from . import views

urlpatterns = [
    #tuesday/
    path('', views.tuesday, name='tuesday')
]