import pytest
from django.contrib.auth.models import User

from blog.models import Post, Comment


@pytest.fixture
def create_user(db):
    user = User.objects.create_user(username='testuser', password='password')
    user.is_superuser = True
    return user


@pytest.fixture
def create_post(create_user):
    return Post.objects.create(title='Test Post', content='Test Content', author=create_user)


@pytest.fixture
def comment(post):
    return Comment.objects.create(author='Test Author', content='Test Comment', post=post)
