from django.shortcuts import redirect, render

# Create your views here.
def index(request):
    return render(request, 'index.html')
    # ana sayfa yazı önerisi

def getProfileBySlug(request, profile_slug):
    profile = Author.objects.get(pk=profile_slug)
    context = {
        'profile': profile
    }
    return render(request, 'profile.html', context)

def getProfileByID(request, profile_id):
    profile = Author.objects.get(pk=profile_id)
    context = {
        'profile': profile
    }
    return render(request, 'profile.html', context)

def getBlogBySlug(request, blog_slug):
    blog = Blog.objects.get(pk=blog_slug)
    context = {
        'blog': blog
    }
    return render(request, 'blog.html', context)

def getBLogById(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    context = {
        'blog': blog
    }
    return render(request, 'blog.html', context)