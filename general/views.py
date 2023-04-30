from django.shortcuts import redirect, render
# import sys
# sys.path.append('../')
from author.models import *

# Create your views here.
def index(request):
    blogs = Blog.objects.all()

    # ana sayfa yazı önerisi
    return render(request, 'general/index.html', {"blogs":blogs})
    

def getProfileBySlug(request, profile_slug):
    profile = Author.objects.get(slug=profile_slug)
    context = {
        'profile': profile
    }
    return render(request, 'general/profile.html', context)

def getProfileByID(request, profile_id):
    profile = Author.objects.get(id=profile_id)
    context = {
        'profile': profile
    }
    return render(request, 'general/profile.html', context)

def getBlogBySlug(request, blog_slug):
    blog = Blog.objects.get(slug=blog_slug)
    context = {
        'blog': blog
    }
    return render(request, 'general/blog.html', context)

def getBLogById(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    context = {
        'blog': blog
    }
    return render(request, 'general/blog.html', context)