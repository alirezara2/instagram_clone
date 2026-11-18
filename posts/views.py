from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import models
from .models import Post, Comment, Like
from .forms import PostCreateForm, CommentForm
from users.models import Follow

def home_view(request):
    if request.user.is_authenticated:
        # پست‌های خودم و کسانی که دنبال می‌کنم
        following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
        posts = Post.objects.filter(
            models.Q(author=request.user) | models.Q(author__in=following_users)
        ).select_related('author', 'author__profile').prefetch_related('likes', 'comments')
    else:
        posts = Post.objects.all().select_related('author', 'author__profile').prefetch_related('likes', 'comments')
    
    context = {
        'posts': posts,
        'comment_form': CommentForm(),
    }
    return render(request, 'posts/home.html', context)

def explore_view(request):
    """صفحه اکسپلور (پست‌های پیشنهادی)"""
    posts = Post.objects.all().select_related('author').prefetch_related('likes')[:30]
    return render(request, 'posts/explore.html', {'posts': posts})

@login_required
def post_create_view(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'پست با موفقیت منتشر شد.')
            return redirect('home')
    else:
        form = PostCreateForm()
    return render(request, 'posts/create_post.html', {'form': form})

@login_required
def post_detail_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().select_related('author')  # type: ignore
    context = {
        'post': post,
        'comments': comments,
        'comment_form': CommentForm(),
    }
    return render(request, 'posts/post_detail.html', context)

@login_required
def post_delete_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author == request.user:
        post.delete()
        messages.success(request, 'پست حذف شد.')
    else:
        messages.error(request, 'شما اجازه حذف این پست را ندارید.')
    return redirect('home')

@login_required
def add_comment_view(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'کامنت ثبت شد.')
    return redirect('post_detail', post_id=post_id)

@login_required
def like_toggle_view(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        return JsonResponse({
            'liked': liked,
            'total_likes': post.likes.count()  # type: ignore
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)