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
from author.forms import PublishForm, UploadForm, EditorForm, BannerPicForm
from author.models import Library, Blog, Author,  Draft
from django.middleware.csrf import get_token
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.template import RequestContext
from account.forms import UpdateAuthorForm, ProfilePicForm, UserForm, AuthorForm, UpdateUserForm





@login_required
def editor(request):
    author = request.user.author
    drafts = author.draft_set.all()
    if request.method == "POST":
        form = EditorForm(request.POST)
        if form.is_valid():
            draft = form.save(commit=False)
            draft.author = author
            draft.save()
            return redirect('editor')
    else:
        form = EditorForm()

    return render(request, 'author/editor.html', {'form': form, 'drafts': drafts})

@login_required
def edit_draft(request, draft_id):
    author = request.user.author
    drafts = author.draft_set.all()
    draft = get_object_or_404(Draft, id=draft_id, author=request.user.author)
    
    try:
        blog = Blog.objects.get(draft=draft)
        NoneBlog = False
    except Blog.DoesNotExist:
        blog = None
        NoneBlog = True

    if request.method == 'POST':
        form = EditorForm(request.POST, instance=draft)

        if form.is_valid():
            draft = form.save(commit=False)
            draft.author = request.user.author
            draft.save()
            if request.POST.get('action') == 'draft':
                return redirect('editor')
            elif request.POST.get('action') == 'publish':
                return redirect('publish', draft_id=draft.id)
            
    else:
        form = EditorForm(instance=draft)

    return render(request, 'author/editor.html', {'form': form, 'draft': draft, 'drafts': drafts, 'blog': blog, 'NoneBlog': NoneBlog})



def panel(request):
    author = request.user.author


    followers = author.followers.all()
    followings = request.user.followings.all()

    followers_count = len(followers)
    followings_count = len(followings)

    return render(request, "author/panel.html", {"author":author, "followers_count":followers_count, "followings_count":followings_count})

def update(request):
    return render(request, "update.html")



def publish(request, draft_id):
    draft = get_object_or_404(Draft, id=draft_id)
    publish_form = PublishForm(initial={"title": draft.title, "text": draft.text})
    bannerpicform = BannerPicForm()
    if request.method == "POST":
        publish_form = PublishForm(request.POST, request.FILES)
        bannerpicform = BannerPicForm(request.POST, request.FILES)
        if publish_form.is_valid() and bannerpicform.is_valid():
            blog = publish_form.save(commit=False)
            blog.author = request.user.author
            blog.draft = draft
            blog.banner = bannerpicform.cleaned_data["banner"]
            blog.save()
            blog.tags.add(*publish_form.cleaned_data["tags"])
            messages.success(request, "Blog post published!")
            return redirect("index")
        
    elif request.method == "GET":
        print("bu sayfaya ulaşamazsın")
    else:
        publish_form = PublishForm(initial={"title": draft.title, "text": draft.text})
        bannerpicform = BannerPicForm()

    return render(
        request,
        "author/publish.html",
        {"publish_form": publish_form, "bannerpicform": bannerpicform},
    )



def upload(request):
    form = UploadForm(request.POST, request.FILES)
    if request.method == "POST":
        if form.is_valid():
            image = Library(image = request.FILES["image"])
            image.save()
    else:
        return render(request, "library.html", {"form":form})


def myblogs(request):
    author = request.user.author
    blogs = Blog.objects.filter(author=author)
    return render(request, "author/myblogs.html", {"blogs":blogs})


def update_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    draft = get_object_or_404(Draft, id=blog.draft.id)
    if request.method == "POST":
        form = PublishForm(request.POST, instance=blog)
        banner = BannerPicForm(request.POST, request.FILES, instance=blog)
        if form.is_valid() and banner.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user.author
            blog.banner = banner.cleaned_data["banner"]
            draft.title = form.cleaned_data["title"]
            draft.text = form.cleaned_data["text"]
            blog.save()
            blog.tags.add(*form.cleaned_data["tags"])
            messages.success(request, "Blog post updated!")
            return redirect("index")
    else:
        form = PublishForm(instance=blog)
        banner = BannerPicForm(instance=blog)
    return render(request, "author/update_blog.html", {"publish_form": form, "bannerpicform": banner})



def update_blog2(request, blog_slug):
    blog = get_object_or_404(Blog, slug=blog_slug)
    draft = get_object_or_404(Draft, id=blog.draft.id)
    if request.method == "POST":
        form = PublishForm(request.POST, instance=blog)
        banner = BannerPicForm(request.POST, request.FILES, instance=blog)
        if form.is_valid() and banner.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user.author
            blog.banner = banner.cleaned_data["banner"]
            draft.title = form.cleaned_data["title"]
            draft.text = form.cleaned_data["text"]
            blog.save()
            blog.tags.add(*form.cleaned_data["tags"])
            messages.success(request, "Blog post updated!")
            return redirect("index")
    else:
        form = PublishForm(instance=blog)
        banner = BannerPicForm(instance=blog)
    return render(request, "author/update_blog.html", {"publish_form": form, "bannerpicform": banner})



def update_draft(request, blog_slug):
    
    blog = get_object_or_404(Blog, slug=blog_slug)
    draft = get_object_or_404(Draft, id=blog.draft.id)
    if request.method == "POST":
        form = EditorForm(request.POST, instance=draft)
        if form.is_valid():
            draft = form.save(commit=False)
            draft.author = request.user.author
            draft.save()
            if request.POST.get('action') == 'draft':
                return redirect('index')
            
            
    else:
        form = EditorForm(instance=draft)
    return render(request, "author/update_draft.html", {"form": form, "draft": draft})

# ilk publish yapildiginda ajax ile alinan form bilgileri bu fonksiyona aktarilir. 
# bu bilgilere gore formlar olusturulur. author/merhaba.html sayfası ve olusturulan formlar
# json formatinda geri dondurulur.
@csrf_exempt
def publish2(request):
    if request.method == "POST":
        title = request.POST.get("title")
        text = request.POST.get("text")
        draft_id = request.POST.get("draft_id")
        print(title, text, draft_id)

        draft = get_object_or_404(Draft, id=draft_id)


        publish_form = PublishForm(instance=draft)
        bannerpicform = BannerPicForm(instance=draft)
        author = request.user.author
        print(title, text, draft_id, author)
        context = {'draft_id': draft_id, 'publish_form': publish_form, 'bannerpicform': bannerpicform}

        html = render(request, 'author/publish2.html', context=context)

        # JSON yanıtı oluşturulması
        data = {'htmlresponse': html.content.decode('utf-8')}
        return JsonResponse(data)
    return JsonResponse({"error": ""})


def publish3(request, draft_id):
    if request.method == "POST":
        publish_form = PublishForm(request.POST, request.FILES)
        bannerpicform = BannerPicForm(request.POST, request.FILES)
        
        if publish_form.is_valid() and bannerpicform.is_valid():
            blog = publish_form.save(commit=False)
            blog.author = request.user.author
            blog.draft_id = draft_id

            blog.save()
            blog.tags.add(*publish_form.cleaned_data["tags"])
            banner = bannerpicform.cleaned_data.get('banner')
            if banner:
                blog.banner = banner
                blog.save()
            

            messages.success(request, "Blog post published!")

            return redirect('index')
    else:
        publish_form = PublishForm()
        bannerpicform = BannerPicForm()
    
    return render(request, 'author/publish2.html', {'publish_form': publish_form, 'bannerpicform': bannerpicform})


@csrf_exempt
def publish4(request):
    if request.method == "POST":
        title = request.POST.get("title")
        text = request.POST.get("text")
        draft_id = request.POST.get("draft_id")
        

        blog = Blog.objects.get(draft=draft_id)
        blog.title = title
        blog.text = text
        
        publish_form = PublishForm(instance=blog)
        bannerpicform = BannerPicForm(instance=blog)
        author = request.user.author
        print(title, text, draft_id, author)
        context = {'draft_id': draft_id, 'publish_form': publish_form, 'bannerpicform': bannerpicform, 'blog': blog}

        html = render(request, 'author/publish4.html', context=context)

        # JSON yanıtı oluşturulması
        data = {'htmlresponse': html.content.decode('utf-8')}
        return JsonResponse(data)
    return JsonResponse({"error": ""})



def delete_post(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    blog.delete()
    messages.success(request, "Blog post deleted!")
    return redirect("index")

@csrf_exempt
def update_author(request):
    if request.user.is_authenticated:
        user = request.user
        author = get_object_or_404(Author, user=user)
        
        
   
    if request.method == "POST":
        print(author.email)
        form = UserForm(request.POST, instance=user)
        author_form = UpdateAuthorForm(instance=author)
        profile_pic_form = ProfilePicForm(instance=author)
        context = {'form': form, 'author_form': author_form, 'profile_pic_form': profile_pic_form}
        print(author)
        html = render(request, 'author/AjaxUpdateAuthor.html', context=context)

        # JSON yanıtı oluşturulması
        data = {'htmlresponse': html.content.decode('utf-8')}
        return JsonResponse(data)
    return JsonResponse({"error": ""})


def update_author2(request):
    if request.user.is_authenticated:
        user = request.user
        author = get_object_or_404(Author, user=user)
        submitted = False
        
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        author_form = UpdateAuthorForm(request.POST, instance=author)
        profile_pic_form = ProfilePicForm(request.POST, request.FILES, instance=author)
        if form.is_valid() and author_form.is_valid() and profile_pic_form.is_valid():
            user = form.save(commit=False)
            author = author_form.save(commit=False)
            profile = profile_pic_form.save(commit=False)
            user.save()
            author.user = user
            author.save()
            profile.author = author
            profile.save()
            update_session_auth_hash(request, user) # Important!
            return redirect("index")
    else:
        form = UserForm(instance=user)
        author_form = UpdateAuthorForm(instance=author, initial={
            'first_name': author.user.first_name,
            'last_name': author.user.last_name,
            'email': author.user.email,
        })
        profile_pic_form = ProfilePicForm(instance=author)
        if "submitted" in request.GET:
            submitted = True

    return render(request, 'author/AjaxUpdateAuthor.html', {'form': form, 'author_form': author_form, 'profile_pic_form': profile_pic_form})


@csrf_exempt
def update_user(request):
    if request.user.is_authenticated:
        user = request.user
        author = get_object_or_404(Author, user=user)
        
        
   
    if request.method == "POST":
        print(author.email)
        
        form = AuthorForm(instance=author)
        user_form = UpdateUserForm(instance=user)
        context = {'form': form, 'user_form': user_form}
        print(author)
        html = render(request, 'author/AjaxUpdateUser.html', context=context)

        # JSON yanıtı oluşturulması
        data = {'htmlresponse': html.content.decode('utf-8')}
        return JsonResponse(data)
    return JsonResponse({"error": ""})

def update_user2(request):
    if request.user.is_authenticated:
        user = request.user
        author = get_object_or_404(Author, user=user)
        submitted = False
        
        if request.method == "POST":
            form = AuthorForm(request.POST.copy(), request.FILES, instance=author)
            user_form = UpdateUserForm(request.POST.copy(), instance=user)
            if form.is_valid() :
                user = user_form.save(commit=False)
                password = user_form.cleaned_data.get('password')
                if password:
                    user.password = make_password(password)
                    user_form.update_session_auth_hash = False
                author = form.save(commit=False)
                
                user.save()
                author.user = user
                author.save()
                
                update_session_auth_hash(request, user)
                
                return redirect("index")
        else:
            form = AuthorForm(instance=author)
            user_form = UpdateUserForm(instance=user)
            if "submitted" in request.GET:
                submitted = True
        return render(request, 'author/AjaxUpdateUser.html', {'form': form, 'user_form': user_form, 'user': user, 'submitted': submitted})
    
def editor2(request, draft_slug):
    author = request.user.author
    drafts = author.draft_set.all()
    draft = get_object_or_404(Draft, slug=draft_slug, author=request.user.author)
    
    try:
        blog = Blog.objects.get(draft=draft)
        NoneBlog = False
    except Blog.DoesNotExist:
        blog = None
        NoneBlog = True

    if request.method == 'POST':
        form = EditorForm(request.POST, instance=draft)

        if form.is_valid():
            draft = form.save(commit=False)
            draft.author = request.user.author
            draft.save()
            if request.POST.get('action') == 'draft':
                return redirect('editor')
            elif request.POST.get('action') == 'publish':
                return redirect('publish', draft_id=draft.id)
            
    else:
        form = EditorForm(instance=draft)

    return render(request, 'author/editor.html', {'form': form, 'draft': draft, 'drafts': drafts, 'blog': blog, 'NoneBlog': NoneBlog})

    
