from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from datetime import date
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import uuid
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import Http404


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, verbose_name="Ad")
    last_name = models.CharField(max_length=50, verbose_name="Soyad")
    email = models.EmailField(max_length=254, verbose_name="E-posta")
    slug = models.SlugField(max_length=50, unique=True, blank=True, null=False, verbose_name="Slug")
    about = models.TextField(max_length=250, verbose_name="Hakkında", blank=True)
    contact = models.URLField(max_length=200, verbose_name="İletişim", blank=True, null=True)
    birthday = models.DateField(verbose_name="Doğum Tarihi", blank=True, null=True)
    img = models.ImageField(upload_to="images", verbose_name="Resim", blank=True, null=True)
    join_date = models.DateField(default=date.today, verbose_name="Katılım Tarihi")
    followers = models.ManyToManyField(User, related_name='followings', symmetrical=False, blank=True)

    class Meta:
        verbose_name_plural = "Yazarlar"
        verbose_name = "Yazar"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user)
        super().save(args, kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def total_followers(self):
        return self.followers.count()

class Draft(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    slug = models.SlugField(default="", blank=True, null=False, unique=True, db_index=True)
    title = models.CharField(max_length=50)
    text = RichTextField( blank=True, null=True )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(uuid.uuid4())
        super().save(*args, **kwargs)

class Library(models.Model):
    image = models.ImageField(upload_to="library/")



class Blog(models.Model):
    title = models.CharField(max_length=50)
    text = RichTextField(blank=True, null=True)
    slug = models.SlugField(default="", blank=True, null=False, unique=True, db_index=True)
    description = models.TextField(max_length=200, blank=True, null=True)
    date = models.DateField(auto_now=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    banner = models.ImageField(upload_to="banners", blank=True, null=True)
    draft = models.ForeignKey(Draft, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='blog_posts')
    tags = TaggableManager()
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(uuid.uuid4())
        super().save(*args, **kwargs)

    def total_likes(self):
        return self.likes.count()

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(blank=True, null=True, max_length=50)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + " " + self.content
    






