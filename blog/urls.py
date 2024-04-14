from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('', views.blog_index, name='blog_index'),
    path('tag/<tag>/', views.blog_tag, name='blog_tag'),
    path('post/<int:pk>/', views.blog_post, name='blog_post'),
    path('addpost/', views.add_post, name='add_post'),
    re_path(r'^froala_editor/', include('froala_editor.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)