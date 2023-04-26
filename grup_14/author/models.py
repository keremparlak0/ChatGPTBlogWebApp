from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from datetime import date

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

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

    class Meta:
        verbose_name_plural = "Yazarlar"
        verbose_name = "Yazar"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Draft(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    text = RichTextField( blank=True, null=True )

class Library(models.Model):
    image = models.ImageField(upload_to="library/")
    

class Blog(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(default="", blank=True, null=False, unique=True, db_index=True)
    description = models.TextField(max_length=200)
    date = models.DateField(auto_now=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    banner = models.ImageField(upload_to="banners")
    draft = models.ForeignKey(Draft, on_delete=models.CASCADE)
    likes = models.PositiveIntegerField()
    tags = TaggableManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(args, kwargs)

