from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from author.forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from author.models import *


def index(request):
    # ana sayfaya giriş
    if request.method == "GET":
        blogs = Blog.objects.all()
        # blog = recommendation   ~Vural
        # ana sayfa yazı öneri algoritması
        return render(request, 'general/index.html', {"blogs":blogs})
    
    # arama işlemi 
    elif request.method == "POST":
        #search()    ~Vural
        pass
    else:
        return HttpResponse("Error")

def search(request):
    pass

def recommendation(request): 
    pass


def getProfileBySlug(request, profile_slug):
    profile = Author.objects.get(slug=profile_slug)
    user = request.user
    
    if Follow.objects.filter(user_id=user, author_id=profile).exists():
        button_name = "Takibi Bırak"
    else:
        button_name = "Takip Et"        

    blogs = {""}
    blogs = Blog.objects.all().filter(author=profile)

    context = {
        'profile': profile,
        'button_name':button_name,
        'blogs':blogs,
    }
    return render(request, 'general/profile.html', context)

def getProfileByID(request, profile_id):
    profile = Author.objects.get(id=profile_id)
    user = request.user   

    if Follow.objects.filter(user_id=user, author_id=profile).exists():
        button_name = "Takibi Bırak"
    else:
        button_name = "Takip Et"        

    blogs = {""}
    blogs = Blog.objects.all().filter(author=profile)

    context = {
        'profile': profile,
        'button_name':button_name,
        'blogs':blogs,
    }
    return render(request, 'general/profile.html', context)

def getBlogBySlug(request, blog_slug):
    blog = Blog.objects.get(slug=blog_slug)
    blog.interaction += 1
    blog.save()

    button_name = "Takip Et" 
    if request.user.is_authenticated and Follow.objects.filter(user_id=request.user, author_id=blog.author).exists():
        button_name = "Takibi Bırak"     

    form = CommentForm()
    comments = Comments.objects.filter(blog_id=blog)
    context = {
        'blog': blog,
        'form': form,
        'comments':comments,
        'button_name':button_name,
    }
    return render(request, 'general/blog.html', context)

def getBLogById(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    blog.interaction += 1
    blog.save()

    button_name = "Takip Et" 
    if request.user.is_authenticated and Follow.objects.filter(user_id=request.user, author_id=blog.author).exists():
        button_name = "Takibi Bırak"

    form = CommentForm()
    comments = Comments.objects.filter(blog_id=blog)
    context = {
        'blog': blog,
        'form':form,
        'comments':comments,
        'button_name':button_name,
    }
    return render(request, 'general/blog.html', context)

def about(request):
    return render(request,"general/about.html")

def contact(request):
    return render(request, "general/contact.html")

@login_required 
def followAction(request, profile_id):
    profile = Author.objects.get(id=profile_id)

    if request.user.is_authenticated:
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
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect("login")
   
    
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



@login_required
def commentAction(request, blog_id=0 ,comment_id=0):
    if request.method == "POST":

        if comment_id==0:
            #create
            blog = Blog.objects.get(pk=blog_id)
            comment = Comments(
                blog_id = blog,
                user_id = request.user,
                message = request.POST["message"]
            )
            comment.save()

        elif blog_id==0:
            #delete
            comment = get_object_or_404(Comments, pk=comment_id)
            if request.user == comment.user_id:
                comment.delete()   
        # else:
        #     #update
        #     pass

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))