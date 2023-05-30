from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
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
            nextUrl = request.GET.get("next",None)
            if nextUrl is None:
                return redirect("index")
            else:
                return redirect(nextUrl)
        else:
            return redirect("index")

    return render(request, "account/login.html")

def register_request(request):
    if request.user.is_authenticated:
        return redirect("index")
        
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]

        if password == repassword:
            if User.objects.filter(username=username).exists():
                return render(request, "account/register.html", 
                {
                    "error":"username kullanılıyor.",
                    "username":username,
                    "email":email,
                    "firstname": firstname,
                    "lastname":lastname
                })
            else:
                if User.objects.filter(email=email).exists():
                    return render(request, "account/register.html", 
                    {
                        "error":"email kullanılıyor.",
                        "username":username,
                        "email":email,
                        "firstname": firstname,
                        "lastname":lastname
                    })
                else:
                    user = User.objects.create_user(username=username,email=email,first_name=firstname,last_name=lastname,password=password)
                    user.save()
                    user = authenticate(username=username, password=password)
                    login(request, user)                
        else:
            return render(request, "account/register.html", {
                "error":"parola eşleşmiyor.",
                "username":username,
                "email":email,
                "firstname": firstname,
                "lastname":lastname
            })

    return render(request, "account/register.html")

def logout_request(request):
    logout(request)
    return redirect("index")

def settings(request):
    return render(request, "account/settings.html")

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# def change_password(request):
#     user = request.user
#     if request.method == "POST":
#         newpassword = request.POST["password"]
#         newrepassword = request.POST["repassword"]
        

#         update_session_auth_hash(request, user)  # Important!
       
#         user.password = newpassword
#         user.password = newrepassword
#         user.save()
        

def change_username(request):
    user = request.user
    if request.method == "POST":
        newusername = request.POST["username"]
        user.username = newusername
        user.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def change_email(request):
    user = request.user
    if request.method == "POST":
        newemail = request.POST["email"]
        user.username = newemail
        user.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove_user(request):
    user = request.user
    logout(request)
    user.delete()
    return redirect("index")