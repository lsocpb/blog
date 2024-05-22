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

    # Test if the tag name is not empty
    def test_tag_name_not_empty(self):
        tag = Tag(name="")
        with pytest.raises(ValidationError):
            tag.full_clean()

    # Test the unique constraint on the tag name field
    def test_tag_name_unique(self):
        Tag.objects.create(name="Django")
        tag = Tag(name="Django")
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

    # Test blank featured_image_url
    def test_post_blank_featured_image_url(self):
        post = Post.objects.create(
            title="No Image Post",
            short_description="This post has no image.",
            content="<p>No image content.</p>",
            featured_image_url="",
            author="Image Tester",
        )
        assert post.featured_image_url == ""

    # Test post creation with multiple tags
    def test_post_multiple_tags(self, tag):
        tag2 = Tag.objects.create(name="Python")
        post = Post.objects.create(
            title="Post with Multiple Tags",
            short_description="This post has multiple tags.",
            content="<p>Multiple tags content.</p>",
            featured_image_url="https://example.com/image4.jpg",
            author="Tag Tester",
        )
        post.tags.add(tag, tag2)
        assert post.tags.count() == 2
        assert tag in post.tags.all()
        assert tag2 in post.tags.all()


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

    # Test the creation of Comment model
    def test_create_comment(self, post):
        comment = Comment.objects.create(
            author="John Doe",
            content="Great post!",
            post=post,
        )
        assert comment.author == "John Doe"
        assert comment.content == "Great post!"
        assert comment.post == post

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

    # Test the cascade delete of comments when a post is deleted
    def test_comment_cascade_delete(self, post):
        comment = Comment.objects.create(
            author="Jane Smith",
            content="Nice article!",
            post=post,
        )
        post.delete()
        assert not Comment.objects.filter(id=comment.id).exists()

    # Test comment content is not empty
    def test_comment_content_not_empty(self, post):
        comment = Comment(author="Jane Doe", content="", post=post)
        with pytest.raises(ValidationError):
            comment.full_clean()

    # Test comment author is not empty
    def test_comment_author_not_empty(self, post):
        comment = Comment(author="", content="Great post!", post=post)
        with pytest.raises(ValidationError):
            comment.full_clean()

    # Test comment ordering
    def test_comment_ordering(self, post):
        comment1 = Comment.objects.create(
            author="Jane Smith",
            content="Nice article!",
            post=post,
        )
        comment2 = Comment.objects.create(
            author="John Doe",
            content="Great post!",
            post=post,
        )
        assert list(post.comment_set.all()) == [comment1, comment2]
        assert list(post.comment_set.all().order_by("-created_at")) == [comment2, comment1]

    # Test comment created_at field
    def test_comment_created_at(self, post):
        comment = Comment.objects.create(
            author="Jane Smith",
            content="Nice article!",
            post=post,
        )
        assert comment.created_at <= timezone.now()
