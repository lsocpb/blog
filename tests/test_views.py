import pytest
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from blog.models import Tag, Comment, Post
from blog.token import token_generator


@pytest.mark.django_db
def test_blog_index_view(client):
    url = reverse('blog_index')
    response = client.get(url)
    assert response.status_code == 200
    assert 'posts' in response.context


@pytest.mark.django_db
def test_blog_tag_view(client, create_post):
    tag = Tag.objects.create(name='testtag')

    create_post.tags.add(tag)
    url = reverse('blog_tag', args=[tag.name])
    response = client.get(url)
    assert response.status_code == 200
    assert 'tag' in response.context
    assert 'posts' in response.context
    assert create_post in response.context['posts']


@pytest.mark.django_db
def test_blog_post_view(client, create_post):
    url = reverse('blog_post', args=[create_post.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert 'post' in response.context
    assert 'comments' in response.context
    assert 'form' in response.context

    # Test adding a comment
    response = client.post(url, data={
        'author': 'Test Author',
        'body': 'Test Comment Body',
    })
    assert response.status_code == 302
    assert Comment.objects.filter(post=create_post).count() == 1


@pytest.mark.django_db
def test_user_login_view(client, create_user):
    url = reverse('login')
    import os
    os.environ['RECAPTCHA_TESTING'] = 'True'

    response = client.get(url)
    print(response)
    print(response.context)
    assert response.status_code == 200
    assert 'loginform' in response.context

    response = client.post(url, data={
        'username': 'testuser',
        'password': 'password',
        'g-recaptcha-response': 'PASSED',
    })
    assert response.status_code == 302
    assert response.url == reverse('blog_index')


@pytest.mark.django_db
def test_add_post_view(client, create_user):
    tag = Tag.objects.create(name='testtag')
    print("Tag id: " + str(tag.id))

    client.login(username='testuser', password='password')
    url = reverse('add_post')
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context

    response = client.post(url, data={
        'title': 'New Test Post',
        'short_description': 'New Test Short Description',
        'featured_image_url': 'https://example.com/image.jpg',
        'content': 'New Test Content',
        'tags': str(tag.id),
        'author': 'Test Author',
    })
    assert response.status_code == 302
    assert Post.objects.filter(title='New Test Post').exists()


@pytest.mark.django_db
def test_edit_post_view(client, create_user, create_post):
    client.login(username='testuser', password='password')
    tag = Tag.objects.create(name='testtag')
    url = reverse('edit_post', args=[create_post.pk])

    print("Tag id: " + str(tag.id))
    response = client.get(url)
    print(response)
    print(response.context)
    assert response.status_code == 200
    assert 'form' in response.context

    response = client.post(url, data={
        'title': 'Updated Test Post',
        'content': 'Updated Test Content',
        'short_description': 'New Test Short Description',
        'tags': str(tag.id),
        'featured_image_url': 'https://example.com/image.jpg',
    })
    assert response.status_code == 302
    create_post.refresh_from_db()
    assert create_post.title == 'Updated Test Post'


@pytest.mark.django_db
def test_delete_post_view(client, create_user, create_post):
    client.login(username='testuser', password='password')
    url = reverse('delete_post', args=[create_post.pk])
    response = client.post(url)
    assert response.status_code == 302
    assert not Post.objects.filter(pk=create_post.pk).exists()


@pytest.mark.django_db
def test_search_posts_view(client, create_post):
    url = reverse('search_posts')
    response = client.get(url, {'q': 'Test'})
    assert response.status_code == 200
    assert 'posts' in response.context
    assert 'query' in response.context
    assert create_post in response.context['posts']


@pytest.mark.django_db
def test_profile_view(client, create_user):
    client.login(username='testuser', password='password')
    url = reverse('profile')
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context


@pytest.mark.django_db
def test_activate_view(client, create_user):
    uid = urlsafe_base64_encode(force_bytes(create_user.pk))
    token = token_generator.make_token(create_user)
    url = reverse('activate', args=[uid, token])
    response = client.get(url)
    assert response.status_code == 302
    create_user.refresh_from_db()
    assert create_user.is_active
