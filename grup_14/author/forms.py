from django import forms
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from author.models import *
from ckeditor.widgets import CKEditorWidget
from taggit.forms import TagWidget

from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User




# class PublishForm(forms.Form):
#     title = forms.CharField(label="Başlık:")
#     description = forms.CharField(widget=forms.Textarea)
#     topics = forms.CharField()
#     cover = forms.CharField()

class PublishForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'description', 'banner']
        labels = {
            "title": "Blog Başlığı",
            "description": "Açıklama",
            "banner" : "Kapak Görseli"

        }
        widgets = {
            "title": forms.TextInput(attrs={"class":"form-control"}),
            "description":forms.Textarea(attrs={"class":"form-control"}),
            "topics" : forms.TextInput(attrs={"class":"form-control"}),
            "banner" : forms.FileInput(attrs={"class":"form-control"}),
        }
        error_messages = {
            "title":{
                "required" : "Blog başlığı girmelisiniz",
                "max_length" : "Başlık uzunluğu maksimum 50 karakter",
            },
            "description" : {
                "required" : "Açıklama bilgisi girilmesi zorunludur."
            }
        }


class UploadForm(forms.ModelForm):
    class Meta:
        model = Library
        fields = ['image']
        labels = {
            "image": "Resim Yükleme Alanı"
        }
        widgets = {
            "image" : forms.FileInput(attrs={"class":"form-control"})
        }
        error_messages = {
            "image":{
                "required" : "Bir resim dosyası yüklemelisiniz"
            }
        }

class EditorForm(forms.ModelForm):

    text = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Draft
        fields = ['title', 'text']
        widgets = {
            'title': forms.TextInput(attrs={"class":"form-control"}),
            'text' : forms.Textarea(attrs={"class":"form-control"})
        }
        

