from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ckeditor.widgets import CKEditorWidget
from taggit.forms import TagWidget
from author.models import *


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            "username": "Username",
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "Email Address",
            "password1": "Password",
            "password2": "Password(tekrar)",
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}),
            "email": forms.TextInput(attrs={"class": "form-control", "placeholder": "Email Address"}),
            "password1": forms.TextInput(attrs={"class": "form-control", "placeholder": "Password"}),
            "password2": forms.TextInput(attrs={"class": "form-control", "placeholder": "Password(tekrar)"}),
        }

class AuthorForm(ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()

    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'email']
        labels = {
            "first_name": "",
            "last_name": "",
            "email": "",
            
        }
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "first name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "last name"}),
            "email": forms.TextInput(attrs={"class": "form-control", "placeholder": "email"}),
           
           
        }

class UpdateUserForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    
    

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',]
        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": " Email Address",
            
            
        }
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "first name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "last name"}),
            "email": forms.TextInput(attrs={"class": "form-control", "placeholder": "email"}),
           
            
        }

class UpdateAuthorForm(ModelForm):

    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'email', 'slug', 'about', 'contact']
        labels = {
            "first_name": "",
            "last_name": "",
            "email": "",
            "slug": "",
            "about": "",
            "contact": "",
          

        }
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "first name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "last name"}),
            "email": forms.TextInput(attrs={"class": "form-control", "placeholder": "email"}),
            "slug": forms.TextInput(attrs={"class": "form-control", "placeholder": "slug"}),
            "about": forms.Textarea(attrs={"class": "form-control", "placeholder": "about"}),
            "contact": forms.Textarea(attrs={"class": "form-control", "placeholder": "contact"}),
                  
        }

class UserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfilePicForm(ModelForm):
    img = forms.ImageField(required=False, widget=forms.FileInput(attrs={"class": "form-control", "placeholder": "profile picture"}))

    class Meta:
        model = Author
        fields = ['img']
        
