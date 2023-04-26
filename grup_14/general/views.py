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

from bs4 import BeautifulSoup
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash

# Create your views here.
def index(request):
    Users = User.objects.all()
    return render(request, 'general/index.html', {'Users': Users})
    # ana sayfa yazı önerisi

def getProfileBySlug(request, profile_slug):
    profile = Author.objects.get(pk=profile_slug)
    context = {
        'profile': profile
    }
    return render(request, 'general/profile.html', context)

def getProfileByID(request, profile_id):
    profile = Author.objects.get(pk=profile_id)
    context = {
        'profile': profile
    }
    return render(request, 'general/profile.html', context)

def getBlogBySlug(request, blog_slug):
    blog = Blog.objects.get(pk=blog_slug)
    context = {
        'blog': blog
    }
    return render(request, 'general/blog.html', context)

def getBLogById(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    context = {
        'blog': blog
    }
    return render(request, 'general/blog.html', context)