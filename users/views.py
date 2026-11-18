from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .forms import RegisterForm, LoginForm, ProfileEditForm
from .models import Profile, CustomUser, Follow

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'ثبت‌نام با موفقیت انجام شد.')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'خوش آمدید {email}!')
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'از حساب خود خارج شدید.')
    return redirect('login')

@login_required
def profile_view(request, email=None):
    if email:
        user = get_object_or_404(CustomUser, email=email)
    else:
        user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    
    # چک کردن فالوو بودن
    is_following = False
    if request.user != user:
        is_following = Follow.objects.filter(follower=request.user, following=user).exists()
    
    context = {
        'profile_user': user,
        'profile': profile,
        'is_own_profile': user == request.user,
        'is_following': is_following,
        'followers_count': user.followers.count(),  # type: ignore
        'following_count': user.following.count(),  # type: ignore
    }
    return render(request, 'users/profile.html', context)

@login_required
def profile_edit_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'پروفایل با موفقیت بروزرسانی شد.')
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=profile)
    return render(request, 'users/edit_profile.html', {'form': form})

@login_required
def search_view(request):
    query = request.GET.get('q', '').strip()
    users = []
    if query:
        users = CustomUser.objects.filter(
            Q(email__icontains=query) | 
            Q(profile__full_name__icontains=query)
        ).exclude(id=request.user.id).distinct()
    return render(request, 'users/search.html', {'query': query, 'users': users})

@login_required
def follow_toggle_view(request, email):
    if request.method == 'POST':
        target_user = get_object_or_404(CustomUser, email=email)
        
        if target_user == request.user:
            return JsonResponse({'error': 'نمی‌توانید خودتان را دنبال کنید'}, status=400)
        
        follow, created = Follow.objects.get_or_create(
            follower=request.user, 
            following=target_user
        )
        
        if not created:
            follow.delete()
            is_following = False
        else:
            is_following = True
            
        return JsonResponse({
            'is_following': is_following,
            'followers_count': target_user.followers.count()  # type: ignore
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)