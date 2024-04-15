from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from blog.models import Post, Comment, Tag
from blog.forms import CommentForm
from blog.forms import CustomUserCreationForm, CustomAuthenticationForm, PostForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth


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


def register(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog_index')

    context = {'registerform': form}
    return render(request, 'blog/templates/blog/register.html', context)


def user_login(request):
    form = CustomAuthenticationForm()
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('blog_index')

    context = {'loginform': form}
    return render(request, 'blog/templates/blog/login.html', context)


def user_logout(request):
    auth.logout(request)
    return redirect('blog_index')


def add_post(request):
    form = PostForm(request.POST or None)
    template_name = 'blog/templates/blog/addpost.html'
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('blog_index')
    context = {'form': form}
    return render(request, template_name, context)


def edit_post(request, pk):
    post = Post.objects.get(pk=pk)
    form = PostForm(request.POST or None, instance=post)
    template_name = 'blog/templates/blog/editpost.html'
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('blog_index')
    context = {'form': form}
    return render(request, template_name, context)
