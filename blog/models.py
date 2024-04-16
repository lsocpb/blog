from django.db import models
from froala_editor.fields import FroalaField


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    short_description = models.TextField()
    content = FroalaField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    featured_image = models.URLField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    visible = models.BooleanField(default=True)
    author = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author} on '{self.post}'"


