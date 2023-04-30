from django import forms
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from author.models import *
from ckeditor.widgets import CKEditorWidget
from taggit.forms import TagWidget

from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'text' : forms.Textarea(attrs={"class":"form-control"})
        }