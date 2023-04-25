from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.

class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30),
    slug = models.SlugField(default="", blank=True, null=False, unique=True, db_index=True),
    about = models.TextField(max_length=250),
    contact = models.URLField(),
    birthday = models.DateField(),
    img = models.ImageField()
    join_date = models.DateField(auto_now=True),

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(args, kwargs)

class Draft(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    text = models.TextField()

class Library(models.Model):
    image = models.ImageField(upload_to="images")
    

class Blog(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(default="", blank=True, null=False, unique=True, db_index=True)
    description = models.TextField(max_length=200)
    topics = models.CharField()
    date = models.DateField(auto_now=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    banner = models.ImageField(upload_to="banners")
    draft = models.ForeignKey(Draft, on_delete=models.CASCADE)
    likes = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(args, kwargs)

