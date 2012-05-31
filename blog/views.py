from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from blog.models import *




def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 5)

    page = request.GET.get('page', 1)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {
        "post_list": posts
        })

@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_staff)
def create(request):
    if request.method == 'POST':
        post = Post()
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post.author = request.user
            post.save()
            return HttpResponseRedirect('/%s' % post.slug)
    else:
        form = PostForm()

    return render(request, 'form.html', {
        'form': form,
        'button': 'Create',
        'title': 'Create a new Post',
    })

def detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'detail.html', {
        'post': post,
        'next': '/%s' % post.slug,
        'author': post.author.get_profile(),
        })

@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_staff)
def edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post.author = request.user
            post.save()
            return HttpResponseRedirect('/%s' % post.slug)
    else:
        form = PostForm(instance=post)

    return render(request, 'form.html', {
        'post': post,
        'form': form,
        'button': 'Save',
        'title': 'Edit the post',
    })

@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_staff)
def delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    return HttpResponseRedirect('/')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user.is_staff = True
            new_user.save()
            new_user = authenticate(
                username=request.POST['username'],
                password=request.POST['password1'])
            login(request, new_user)
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()

    return render(request, "signup.html", {
        'form' : form
    })

@login_required(login_url='/login')
def profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserChangeForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES,
            instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            request.user.save()
            profile.save()
            print profile.avatar
            return HttpResponseRedirect("/")
    else:
        user_form = UserChangeForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)

    return render(request, "profile.html", {
        "user_form": user_form,
        "profile_form": profile_form,
        })
