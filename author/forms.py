from django import forms

from author.models import *

# class PublishForm(forms.Form):
#     title = forms.CharField(label="Başlık:")
#     description = forms.CharField(widget=forms.Textarea)
#     topics = forms.CharField()
#     cover = forms.CharField()

class PublishForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'description', 'topics', 'banner', 'text']
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

class Editor(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['content']
        widgets = {
            'content' : RichTextFormField(config_name="default")
        }
        

