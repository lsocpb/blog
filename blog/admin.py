from django.contrib import admin
from blog.models import Post, Tag, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ['title']


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_at')
    search_fields = ['author']


# Register your models here.

admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
