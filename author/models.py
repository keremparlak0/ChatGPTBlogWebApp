from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

class Author(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250)
    about = models.CharField(default="", null=True, max_length=500)
    contact = models.CharField(default="",null=True, max_length=200)
    birthday = models.DateField(blank=True, null=True)
    picture = models.ImageField(blank=True, upload_to="pictures/")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super().save(args, kwargs)

    @property
    def author_id(self):
        return self.id

class Draft(models.Model):
    
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = RichTextUploadingField()
    def __str__(self):
        return self.title
    
    @property
    def draft_id(self):
        return self.id

class Blog(models.Model):
    draft = models.ForeignKey(Draft, on_delete=models.CASCADE)
    banner = models.ImageField(upload_to="banners/")
    slug = models.SlugField(default="", blank=True, null=False, unique=True, db_index=True)
    description = models.TextField(max_length=250)
    tags = models.CharField(max_length=500)
    date = models.DateField(auto_now=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    like_count = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.draft.title)
        super().save(args, kwargs)

    @property
    def blog_id(self):
        return self.id

class Follow(models.Model):
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)  #following
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)      #followers

    @property
    def follow_id(self):
        return self.id

class Comments(models.Model):
    blog_id = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=500)
    date = models.DateField(auto_now=True)

    @property
    def comment_id(self):
        return self.id


