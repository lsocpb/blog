import pytest
from django.utils import timezone
from blog.models import Tag, Post, Comment
from django.core.exceptions import ValidationError


@pytest.mark.django_db
class TestTagModel:
    # Test the string representation of the Tag model
    def test_tag_string_representation(self):
        tag = Tag.objects.create(name="Python")
        assert str(tag) == "Python"

    # Test the created_at field of the Tag model
    def test_create_tag(self):
        tag = Tag.objects.create(name="Django")
        assert tag.name == "Django"

    # Test max length of the tag field
    def test_tag_name_max_length(self):
        tag = Tag(name="A" * 51)
        with pytest.raises(ValidationError):
            tag.full_clean()


@pytest.mark.django_db
class TestPostModel:
    @pytest.fixture
    def tag(self):
        return Tag.objects.create(name="Django")

    # Test the string representation of the Post model
    def test_post_string_representation(self, tag):
        post = Post.objects.create(
            title="My First Post",
            short_description="This is my first blog post.",
            content="<p>Hello, World!</p>",
            featured_image_url="https://example.com/image.jpg",
            author="John Doe",
        )
        assert str(post) == "My First Post"

    # Test the relationship between Post and Tag models
    def test_post_tags(self, tag):
        post = Post.objects.create(
            title="Another Post",
            short_description="Another blog post.",
            content="<p>Hello again!</p>",
            featured_image_url="https://example.com/image2.jpg",
            author="Jane Smith",
        )
        post.tags.add(tag)
        assert post.tags.count() == 1
        assert tag in post.tags.all()

    # Test the creation of Post model
    def test_create_post(self):
        post = Post.objects.create(
            title="Yet Another Post",
            short_description="Yet another blog post.",
            content="<p>Hello, one more time!</p>",
            featured_image_url="https://example.com/image3.jpg",
            author="John Smith",
        )
        assert post.created_at <= timezone.now()
        assert post.visible is True
        assert post.author == "John Smith"
        assert post.featured_image_url == "https://example.com/image3.jpg"
        assert post.content == "<p>Hello, one more time!</p>"
        assert post.short_description == "Yet another blog post."
        assert post.title == "Yet Another Post"

    # Test the max length of the title field
    def test_post_title_max_length(self):
        post = Post(title="A" * 256)
        with pytest.raises(ValidationError):
            post.full_clean()

    # Test the max length of the author field
    def test_post_author_max_length(self):
        post = Post(author="A" * 51)
        with pytest.raises(ValidationError):
            post.full_clean()


@pytest.mark.django_db
class TestCommentModel:
    @pytest.fixture
    def post(self):
        return Post.objects.create(
            title="Test Post",
            short_description="Post for testing comments.",
            content="<p>This is a test post.</p>",
            featured_image_url="https://example.com/image3.jpg",
            author="Test User",
        )

    # Test the string representation of the Comment model
    def test_comment_string_representation(self, post):
        comment = Comment.objects.create(
            author="John Doe",
            content="Great post!",
            post=post,
        )
        assert str(comment) == "John Doe on 'Test Post'"

    # Test the relationship between Comment and Post models
    def test_comment_post_relationship(self, post):
        comment = Comment.objects.create(
            author="Jane Smith",
            content="Nice article!",
            post=post,
        )
        assert comment.post == post

    # Test the max length of the author field
    def test_comment_author_max_length(self, post):
        comment = Comment(author="A" * 51, content="Great post!", post=post)
        with pytest.raises(ValidationError):
            comment.full_clean()