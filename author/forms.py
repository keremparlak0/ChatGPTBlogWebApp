from django import forms
from ckeditor.widgets import CKEditorWidget
from author.models import *

# Blog Model Form
class PublishForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'description', 'tags', 'banner']
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

# Library Model Form
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

# Draft Model Form
class Editor(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Draft
        fields = ['content']
        

# Author Model Form
class UpdateForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['about','contact','birthday','picture']


# Follow Model Form
class FollowForm(forms.ModelForm):
    class Meta:
        model = Follow
        fields = '__all__'



# Comment Model Form
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = '__all__'
