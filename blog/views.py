from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView, RedirectView, TemplateView

from blog.models import Post, Comment, Tag
from blog.forms import CommentForm, SignUpForm, user_model
from blog.forms import CustomAuthenticationForm, PostForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth

from blog.token import token_generator


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


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'blog/templates/blog/register.html'
    success_url = reverse_lazy('check_email')

    def form_valid(self, form):
        to_return = super().form_valid(form)

        user = form.save()
        user.is_active = False
        user.save()

        form.send_activation_email(self.request, user)

        return to_return

class ActivateView(RedirectView):

    url = reverse_lazy('blog_index')

    # Custom get method
    def get(self, request, uidb64, token):

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = user_model.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, user_model.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return super().get(request, uidb64, token)
        else:
            return render(request, 'blog/templates/blog/activate_invalid.html')

class CheckEmailView(TemplateView):
    template_name = 'blog/templates/blog/check_email.html'

class SuccessView(TemplateView):
    template_name = 'blog/templates/blog/index.html'

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


@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.username
            post.save()
            form.save_m2m()
            return redirect('blog_index')
        else:
            print(form.errors)
    else:
        form = PostForm()
    return render(request, 'blog/templates/blog/addpost.html', {'form': form})


@login_required()
def edit_post(request, pk):
    if request.user != Post.objects.get(pk=pk).author and not request.user.is_superuser:
        return redirect('blog_index')

    post = Post.objects.get(pk=pk)
    form = PostForm(request.POST or None, instance=post)
    template_name = 'blog/templates/blog/editpost.html'
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('blog_index')
        else:
            print(form.errors)
    context = {'form': form}
    return render(request, template_name, context)


@login_required
def delete_post(request, pk):
    if request.user != Post.objects.get(pk=pk).author and not request.user.is_superuser:
        return redirect('blog_index')

    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect('blog_index')


def search_posts(request):
    query = request.GET.get('q', '')
    posts = Post.objects.filter(title__icontains=query)
    context = {
        'posts': posts,
        'query': query,
    }
    return render(request, 'blog/templates/blog/search.html', context)