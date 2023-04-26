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
from .forms import RegisterUserForm, AuthorForm, UpdateUserForm, UpdateAuthorForm, UserForm, ProfilePicForm
from bs4 import BeautifulSoup
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash



def login_request(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, f' Hoşgeldiniz {user.first_name}!')
            return redirect("index")
        else:
            messages.info(request, 'Kullanıcı adı veya şifre hatalı! Lütfen tekrar deneyiniz.')
            return redirect('login')

    return render(request, "account/login.html")






def register_request(request):
    if request.user.is_authenticated:
        return redirect("index")
    
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        author_form = AuthorForm(request.POST)
        if form.is_valid() and author_form.is_valid():
            authorsave = form.save()
            author = author_form.save(commit=False)
            author.user = authorsave
            author.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            
            user = authenticate(username=username, password=password)
            
            
            login(request, user)

            messages.success(request, f'Account created for {user.first_name}')
            return redirect('index')
    else:
        form = RegisterUserForm()
        author_form = AuthorForm()
    
    return render(request, 'account/register.html', {'form': form})



def logout_request(request):
    logout(request)
    messages.success(request, ' You have been logged out! ')
    return redirect('login')


@login_required    
def update_request(request):
    if request.user.is_authenticated:
        user = request.user
        author = get_object_or_404(Author, user=user)
        submitted = False
        
        if request.method == "POST":
            form = AuthorForm(request.POST.copy(), request.FILES, instance=author)
            if form.is_valid():
                form.save()
                user_form = UpdateUserForm(request.POST.copy(), instance=user)
                if user_form.is_valid():
                    user = user_form.save(commit=False)
                    password = user_form.cleaned_data.get('password')
                    if password:
                        user.password = make_password(password)
                        user_form.update_session_auth_hash = False
                    user.save()
                    update_session_auth_hash(request, user) # Important!
                    return redirect("index")
        else:
            form = AuthorForm(instance=author)
            user_form = UpdateUserForm(instance=user)
            if "submitted" in request.GET:
                submitted = True
        return render(request, 'account/update_user.html', {'form': form, 'user_form': user_form, 'user': user, 'submitted': submitted})
    


@login_required    
def update_author_request(request):
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
            author_form = UpdateAuthorForm(instance=author)
            profile_pic_form = ProfilePicForm(instance=author)
            if "submitted" in request.GET:
                submitted = True
        return render(request, 'account/update_author.html', {'form': form, 'author_form': author_form, 'profile_pic_form': profile_pic_form, 'user': user, "submitted": submitted})
