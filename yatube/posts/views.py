from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from posts.forms import PostForm

from .models import Group, Post

User = get_user_model()
Posts_on_page = 10


def get_page_context(request, queryset):
    paginator = Paginator(queryset, Posts_on_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return {
        'page_obj': page_obj,
    }


def index(request):
    posts = Post.objects.all()
    context = get_page_context(request, posts)
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    context = {
        'group': group
    }
    context.update(get_page_context(request, posts))
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    context = {
        'author': author
    }
    context.update(get_page_context(request, posts))
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {
        'post': post
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(data=request.POST or None)

    if request.method != 'POST':
        return render(request, 'posts/post_create.html', {'form': form})

    if not form.is_valid():
        return render(request, 'posts/post_create.html', {'form': form})

    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect('posts:profile', post.author)


@login_required
def post_edit(request, post_id):
    post_edit = get_object_or_404(Post, pk=post_id)
    form = PostForm(request.POST or None, instance=post_edit)

    if post_edit.author != request.user:
        return redirect('posts:post_detail', post_id)

    if request.method != 'POST' or not form.is_valid():
        form = PostForm(instance=post_edit)
        return render(
            request, 'posts/post_create.html',
            {
                'form': form,
                'post_id': post_id,
                'post_edit': post_edit
            }
        )

    form.save()
    return redirect('posts:post_detail', post_id)
