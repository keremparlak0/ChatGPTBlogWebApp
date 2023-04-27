from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


# Create your models here.

class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(default="", blank=True, null=False, unique=True, db_index=True),
    about = models.TextField(max_length=250, default="", blank=True, null=True),
    contact = models.URLField(default="", blank=True, null=True),
    birthday = models.DateField(default="", blank=True, null=True),
    picture = models.ImageField(default="", blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(args, kwargs)

class Draft(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = RichTextField()

class Library(models.Model):
    image = models.ImageField(upload_to="images")
    
class Blog(models.Model):
    draft = models.ForeignKey(Draft, on_delete=models.CASCADE)
    banner = models.ImageField(upload_to="banners")
    title = models.CharField(max_length=50)
    slug = models.SlugField(default="", blank=True, null=False, unique=True, db_index=True)
    description = models.TextField(max_length=250)
    tags = models.CharField(max_length=500)
    date = models.DateField(auto_now=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    like_count = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(args, kwargs)

class Follow(models.Model):
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)  #following
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)      #followers

class Comments(models.Model):
    blog_id = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=500)
    date = models.DateField(auto_now=True)


