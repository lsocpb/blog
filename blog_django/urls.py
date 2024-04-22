"""
URL configuration for blog_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from blog.views import user_login, user_logout, add_post
from blog.views import (
    SignUpView,
    ActivateView,
    CheckEmailView,
    SuccessView,
    ProfileView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('register/', SignUpView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name="activate"),
    path('check-email/', CheckEmailView.as_view(), name="check_email"),
    path('success/', SuccessView.as_view(), name="success"),
    path('accounts/login/', user_login, name='login'),
    path('accounts/logout/', user_logout, name='logout'),
    path('addpost/', add_post, name='addpost'),
    path('profile/', ProfileView.as_view(), name='profile'),
    re_path(r'^froala_editor/', include('froala_editor.urls')),
]
