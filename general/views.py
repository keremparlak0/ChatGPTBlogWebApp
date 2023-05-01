from django.shortcuts import redirect, render
from author.forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from author.models import *

def index(request):
    blogs = Blog.objects.all()
    
    # ana sayfa yazı öneri algoritması
    return render(request, 'general/index.html', {"blogs":blogs})
    

def getProfileBySlug(request, profile_slug):
    profile = Author.objects.get(slug=profile_slug)
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            follow(request,profile)
        else:
            return redirect("login")
            
    is_follow = Follow.objects.check(user_id=request.user, author_id=profile)    
    if Follow.objects.filter(user_id=request.user, author_id=profile).exists():
        button_name = "Unfollow"
    else:
        button_name = "follow"      

    context = {
        'profile': profile,
        'button_name':button_name,
    }
    return render(request, 'general/profile.html', context)

def getProfileByID(request, profile_id):
    profile = Author.objects.get(id=profile_id)
    if request.method == 'POST':
        if request.user.is_authenticated:
            follow(request,profile)
        else:
            return redirect("login")

    if Follow.objects.filter(user_id=request.user, author_id=profile).exists():
        button_name = "Unfollow"
    else:
        button_name = "follow"        

    context = {
        'profile': profile,
        'button_name':button_name,
    }
    return render(request, 'general/profile.html', context)

def getBlogBySlug(request, blog_slug):
    blog = Blog.objects.get(slug=blog_slug)
    blog.interaction += 1
    blog.save()
    form = CommentForm()
    comments = Comments.objects.filter(blog_id=blog)
    context = {
        'blog': blog,
        'form': form,
        'comments':comments
    }
    return render(request, 'general/blog.html', context)

def getBLogById(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    blog.interaction += 1
    blog.save()
    form = CommentForm()
    comments = Comments.objects.filter(blog_id=blog)
    context = {
        'blog': blog,
        'form':form,
        'comments':comments,
    }
    return render(request, 'general/blog.html', context)


@login_required
def comment(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user_id = request.user
            comment.blog_id = blog
            comment.save()
            return redirect('/blog/'+str(blog_id))
    else:
        form = CommentForm()
    return render(request, 'general/comment.html', {'form': form})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comments, pk=comment_id)
    blog = comment.blog_id
    if request.user == comment.user_id:
        comment.delete()
        
    return redirect('blogbyslug',blog.slug)

# @login_required
# def edit_comment(request, comment_id):
#     comment = get_object_or_404(Comments, pk=comment_id)
#     if request.user == comment.user_id:
#         if request.method == 'POST':
#             form = CommentForm(request.POST, instance=comment)
#             if form.is_valid():
#                 comment = form.save(commit=False)
#                 comment.name = request.user
#                 comment.save()
#                 return redirect('/blog/'+str(comment.blog.id))
#         else:
#             form = CommentForm(instance=comment)
#         return render(request, 'general/comment.html', {'form': form})
#     else:
#         return redirect('/blog/'+str(comment.blog.id))
    
def follow(request, profile):
    try:
        #if follow exist
        follow = Follow.objects.get(user_id=request.user, author_id=profile)
        follow.delete()
        print("follow deleted")
    except:
        #if follow does not exist
        newfollow = Follow(
        user_id = request.user,
        author_id = profile,
        )
        newfollow.save()
        print("follow created")
    return

    
@login_required
def like(request, blog_id):
    blog = Blog.objects.get(pk=request.POST.get('blog_id'))
    liked = False
    if blog.likes.filter(id=request.user.id).exists():
        blog.likes.remove(request.user)
        liked = False
    else:
        liked = True
        blog.likes.add(request.user)
    
    return redirect('blogbyslug',blog.slug)
