from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from api.models import *
from api.serializer import *

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import *

# def re-captcha(request):

# def password-recovery(request):

# def email-validation(request):

# def change-password(request):

# def change-username(request):

# def change-email(request):

def login_request(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username = username, password = password)

    return Response(status=HTTP_204_NO_CONTENT)

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
                    return redirect("index")                    
        else:
            return render(request, "account/register.html", {
                "error":"parola eşleşmiyor.",
                "username":username,
                "email":email,
                "firstname": firstname,
                "lastname":lastname
            })

    return Response(status=HTTP_204_NO_CONTENT)

def logout_request(request):
    logout(request)
    return Response(status=HTTP_204_NO_CONTENT)


def is_author():
    pass

def author(request, id=0):
    if request.method == "GET":
        #read
        pass
    elif request.method == "POST":
        #create
        user = request.user
        user.is_staff=True
        pass
    elif request.method == "PUT":
        #update
        pass
    elif request.method == "DELETE":
        #delete
        user = request.user
        user.is_staff=False
        pass
    else:
        return

@login_required()
def draft(request, id=0):
    if request.method == "GET":
        #read
        pass
    elif request.method == "POST":
        #create
        author = Author.objects.get(user = request.user)
        draft = Draft(content = "", title="", author = author)
        serializer = serializers(draft)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)
    elif request.method == "PUT":
        #update
        draft = get_object_or_404(Draft, pk=id)
        author = Author.objects.get(user = request.user)
        if draft.author != author:
            return Response({"error":"unauthorized access"}, status=HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    
        serializer = DraftSerializer(draft, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    elif request.method == "DELETE":
        #delete
            draft = get_object_or_404(Draft, pk=id)
    author = Author.objects.get(user = request.user)


    # if the author doesn't own this draft
    if draft.author != author:
        return Response({"error":"unauthorized access"}, status=HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    draft.delete()
    return Response(status=HTTP_204_NO_CONTENT)


def blog(request, id=0):
    if request.method == "GET":
        #read
        pass
    elif request.method == "POST":
        #create
        pass
    elif request.method == "PUT":
        #update
        pass
    elif request.method == "DELETE":
        #delete
        pass


def follow(request, id=0):
    pass


def comment(request, id=0):
    if request.method == "GET":
        #read
        pass
    elif request.method == "POST":
        #create
        pass
    elif request.method == "PUT":
        #update
        pass
    elif request.method == "DELETE":
        #delete
        pass