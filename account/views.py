from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

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
                    return redirect("login")                    
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

# def re-captcha(request):

# def password-recovery(request):

# def email-validation(request):

# def change-password(request):

# def change-username(request):

# def change-email(request):
