from django.shortcuts import render
from django.http import HttpResponseRedirect
from blog.models import Post, Comment, Tag
from blog.forms import CommentForm


def blog_index(request):
    posts = Post.objects.all().order_by('-created_at')
    context = {
        'posts': posts,
    }
    return render(request, 'blog/templates/blog/index.html', context)


def blog_tag(request, tag):
    posts = Post.objects.filter(tags__name__contains=tag).order_by('-created_at')
    context = {
        'tag': tag,
        'posts': posts,
    }
    return render(request, 'blog/templates/blog/tag.html', context)


def blog_post(request, pk):
    post = Post.objects.get(pk=pk)
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                content=form.cleaned_data["body"],
                post=post,
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)

    comments = Comment.objects.filter(post=post)
    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }
    return render(request, 'blog/templates/blog/post.html', context)
