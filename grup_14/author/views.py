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
from author.forms import PublishForm, UploadForm, EditorForm
from author.models import Library, Blog, Author,   Draft



def editor(request):
    author = request.user.author
    if request.method == 'POST':
        form = EditorForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = author.user
            post.save()
            return redirect("index")
    else:
        form = EditorForm()

    return render(request, 'author/editor.html', {'form': form})




def panel(request):
    author = request.user.author
    return render(request, "author/panel.html", {"author":author})

def update(request):
    return render(request, "update.html")

def publish(request):
    if request.method == "POST":
        form = PublishForm()

        if form.is_valid():
            blog = Blog(title=form.cleaned_data["title"], 
                        description=form.cleaned_data["description"],
            
                        )
            blog.save()
            return redirect("/author/panel")

    else:
        form = PublishForm()

    return render(request, "publish.html", {"form":form})

def upload(request):
    form = UploadForm(request.POST, request.FILES)
    if request.method == "POST":
        if form.is_valid():
            image = Library(image = request.FILES["image"])
            image.save()
    else:
        return render(request, "library.html", {"form":form})