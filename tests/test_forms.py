from django.contrib.auth import get_user_model
from django.test import TestCase

from blog.forms import (
    CommentForm,
    SignUpForm,
    CustomAuthenticationForm,
    PostForm,
    ProfileForm,
    ResetPasswordForm,
    NewPasswordForm
)
from blog.models import Tag

User = get_user_model()


class CommentFormTest(TestCase):
    def test_valid_comment_form(self):
        form = CommentForm(data={'author': 'Test Author', 'body': 'This is a test comment.'})
        self.assertTrue(form.is_valid())

    def test_invalid_comment_form(self):
        form = CommentForm(data={'author': '', 'body': ''})
        self.assertFalse(form.is_valid())


class SignUpFormTest(TestCase):
    def setUp(self):
        import os
        os.environ['RECAPTCHA_TESTING'] = 'True'

    def test_valid_signup_form(self):
        form = SignUpForm(data={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123',
        })
        self.assertTrue(form.is_valid())

    def test_invalid_signup_form(self):
        form = SignUpForm(data={
            'username': 'testuser',
            'email': 'invalidemail',
            'password1': 'TestPassword123',
            'password2': 'DifferentPassword123',
        })
        self.assertFalse(form.is_valid())


class CustomAuthenticationFormTest(TestCase):
    def setUp(self):
        import os
        os.environ['RECAPTCHA_TESTING'] = 'True'

    def test_valid_authentication_form(self):
        user = User.objects.create_user(username='testuser', password='TestPassword123')
        form = CustomAuthenticationForm(data={'username': 'testuser', 'password': 'TestPassword123'})
        self.assertTrue(form.is_valid())

    def test_invalid_authentication_form(self):
        form = CustomAuthenticationForm(data={'username': 'testuser', 'password': 'WrongPassword'})
        self.assertFalse(form.is_valid())


class PostFormTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name='Test Tag')

    def test_valid_post_form(self):
        form = PostForm(data={
            'title': 'Test Title',
            'short_description': 'Test Short Description',
            'content': 'Test Content',
            'tags': [self.tag.id],
            'featured_image_url': 'http://example.com/image.jpg'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_post_form(self):
        form = PostForm(
            data={'title': '', 'short_description': '', 'content': '', 'tags': [], 'featured_image_url': ''})
        self.assertFalse(form.is_valid())


class ProfileFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com')

    def test_valid_profile_form(self):
        form = ProfileForm(instance=self.user, data={'username': 'updateduser', 'email': 'updateduser@example.com'})
        self.assertTrue(form.is_valid())

    def test_invalid_profile_form(self):
        form = ProfileForm(instance=self.user, data={'username': '', 'email': 'invalidemail'})
        self.assertFalse(form.is_valid())


class ResetPasswordFormTest(TestCase):

    def test_valid_reset_password_form(self):
        form = ResetPasswordForm(data={'email': 'testuser@example.com'})
        self.assertTrue(form.is_valid())

    def test_invalid_reset_password_form(self):
        form = ResetPasswordForm(data={'email': 'invalidemail'})
        self.assertFalse(form.is_valid())


class NewPasswordFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='OldPassword123')
        import os
        os.environ['RECAPTCHA_TESTING'] = 'True'

    def test_valid_new_password_form(self):
        form = NewPasswordForm(user=self.user, data={
            'new_password1': 'NewPassword123',
            'new_password2': 'NewPassword123'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_new_password_form(self):
        form = NewPasswordForm(user=self.user, data={
            'new_password1': 'NewPassword123',
            'new_password2': 'DifferentPassword123'
        })
        self.assertFalse(form.is_valid())
