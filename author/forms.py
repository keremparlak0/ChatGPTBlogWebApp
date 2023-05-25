from django import forms
from ckeditor.widgets import CKEditorWidget
from author.models import *

# Blog Model Form
class PublishForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['description', 'tags', 'banner']
        labels = {
            "description": "Açıklama",
            "banner" : "Kapak Görseli",
            "tags" : "etiketler",

        }
        widgets = {
            "description":forms.Textarea(attrs={"class":"form-control"}),
            "tags" : forms.TextInput(attrs={"class":"form-control"}),
            "banner" : forms.FileInput(attrs={"class":"form-control"}),
        }


# Library Model Form
# class UploadForm(forms.ModelForm):
#     class Meta:
#         model = Library
#         fields = ['image']
#         labels = {
#             "image": "Resim Yükleme Alanı"
#         }
#         widgets = {
#             "image" : forms.FileInput(attrs={"class":"form-control"})
#         }
#         error_messages = {
#             "image":{
#                 "required" : "Bir resim dosyası yüklemelisiniz"
#             }
#         }

# Draft Model Form
class Editor(forms.ModelForm):
    #content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Draft
        fields = ['title','content']
        widgets = {
            "title": forms.TextInput(attrs={"class":"form-control"}),
            "content": CKEditorWidget(),
        }
        

# Author Model Form
class UpdateForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['about','contact','birthday','picture']
        labels = {
            "about": "Hakkımda: ",
            "contact": "İletişim: ",
            "birthday": "doğum tarihi:(YYYY-MM-DD)",
            "picture" : "Profil Görseli: ",
        }
        widgets = {
            "about": forms.TextInput(attrs={"class":"form-control"}),
            "contact": forms.TextInput(attrs={"class":"form-control"}),
            "birthday" : forms.DateInput(attrs={"class":"form-control"}),
            "picture" : forms.FileInput(attrs={"class":"form-control"}),
        }

# Follow Model Form



# Comment Model Form
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['message']
        widgets = {
            'text' : forms.Textarea(attrs={"class":"form-control"})
        }
        labels = {
            "message": "mesaj: ",

        }
