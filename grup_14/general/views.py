from django.shortcuts import redirect, render
from author.models import Author, Blog
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai
import requests
from django.http import HttpResponse
from django.utils.text import slugify
from author.models import Library, Blog, Author,   Draft, Comment
from bs4 import BeautifulSoup
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash
from .forms import CommentForm
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseBadRequest


# Create your views here.
def index(request):
    Users = User.objects.all()
    posts = Blog.objects.all()
    
    return render(request, 'general/index.html', {'Users': Users, 'posts': posts})
    # ana sayfa yazı önerisi

def getProfileBySlug(request, profile_slug):

    
    author = Author.objects.get(slug=profile_slug)
    author_user = author.user
    followers = author.followers.all()
    
    followings = author_user.followings.all()

    user_id = request.user.id
    user_followers = len(author.followers.filter(pk=user_id))

    followers_count = len(followers)
    followings_count = len(followings)

    if user_followers == 1:
        follow_button_value = 'unfollow'
    else:
        follow_button_value = 'follow'

    context = {
        'author': author,
        'followers': followers,
        'user_followers': user_followers,
        'followers_count': followers_count,
        'follow_button_value': follow_button_value,
        'followings_count': followings_count

    }
    return render(request, 'general/profile.html', context)

def getProfileByID(request, profile_id):
    author = Author.objects.get(pk=profile_id)
    followers = author.followers.all()
    
    user_id = request.user.id
    user_followers = len(author.followers.filter(pk=user_id))

    followers_count = len(followers)

    if user_followers == 1:
        follow_button_value = 'unfollow'
    else:
        follow_button_value = 'follow'

    context = {
        'author': author,
        'followers': followers,
        'user_followers': user_followers,
        'followers_count': followers_count,
        'follow_button_value': follow_button_value

    }
    return render(request, 'general/profile.html', context)

def getBlogBySlug(request, blog_slug):
    blog = Blog.objects.get(slug=blog_slug)
    form = CommentForm()
    comments = Comment.objects.filter(blog=blog)
    context = {
        'blog': blog,
        'form': form,
        'comments': comments
    }
    return render(request, 'general/blog.html', context)

def getBLogById(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    form = CommentForm()
    comments = Comment.objects.filter(blog=blog)
    context = {
        'blog': blog,
        'form': form,
        'comments': comments
    }
    return render(request, 'general/blog.html', context)
    
def comment(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.name = request.user
            comment.blog = blog
            comment.save()
            return redirect('/blog/'+str(blog_id))
    else:
        form = CommentForm()
    return render(request, 'general/comment.html', {'form': form})
    
def like(request, blog_id):
    blog = Blog.objects.get(pk=request.POST.get('blog_id'))
    liked = False
    if blog.likes.filter(id=request.user.id).exists():
        blog.likes.remove(request.user)
        liked = False
    else:
        liked = True
        blog.likes.add(request.user)
    

    return redirect('/blog/'+str(blog_id))

@csrf_exempt
def followers_count(request):
    if request.method == 'POST':
        user_id = request.POST.get('user')
        follower_id = request.POST.get('follower')
        value = request.POST.get('value')
        author = Author.objects.get(pk=follower_id)
        if value == 'follow':
            author.followers.add(user_id)
            author.save()
            return redirect('/profile/'+str(author.slug))
        else:
            author.followers.remove(user_id)
            author.save()
            return redirect('/profile/'+str(author.slug))
    

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user.username == comment.name:
        comment.delete()
        
    return redirect('/blog/'+str(comment.blog.id))