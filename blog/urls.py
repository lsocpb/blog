from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_index, name='blog_index'),
    path('tag/<tag>/', views.blog_tag, name='blog_tag'),
    path('post/<int:pk>/', views.blog_post, name='blog_post'),
]