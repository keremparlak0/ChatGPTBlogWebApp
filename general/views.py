from django.shortcuts import redirect, render
from author.forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from author.models import *

# import sys
# sys.path.append('../')


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
    blog.interaction += 1
    blog.save()
    context = {
        'blog': blog
    }
    return render(request, 'general/blog.html', context)

def getBLogById(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    blog.interaction += 1
    blog.save()
    context = {
        'blog': blog
    }
    return render(request, 'general/blog.html', context)


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


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comments, pk=comment_id)
    if request.user.username == comment.name:
        comment.delete()
        
    return redirect('/blog/'+str(comment.blog.id))

def edit_comment(request, comment_id):
    comment = get_object_or_404(Comments, pk=comment_id)
    if request.user.username == comment.name:
        if request.method == 'POST':
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.name = request.user
                comment.save()
                return redirect('/blog/'+str(comment.blog.id))
        else:
            form = CommentForm(instance=comment)
        return render(request, 'general/comment.html', {'form': form})
    else:
        return redirect('/blog/'+str(comment.blog.id))
    

def follow(request, profile_id):
    user = request.user
    author = Author(pk=profile_id)
    form = FollowForm()
    if request.method == 'POST':
        form = FollowForm(request.POST)
        if form.is_valid():
            follow = form.save(commit=False)
            follow.user_id = user
            follow.author_id = author
            follow.save()
            return redirect('/profile/'+str(profile_id))

    
    