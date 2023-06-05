from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from django.contrib.postgres.search import SearchVector
from django.contrib.postgres.indexes import GinIndex
from general.zemberekkk import MyService
from bs4 import BeautifulSoup
from taggit.models import Tag, TaggedItem
from django.contrib.postgres.search import SearchVectorField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.search import SearchVector
from django.db.models import Count

# user profil fotoğrafı için
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='pictures/', blank=True, null=True, default='{% static "img/profil.png" %}')
    # Diğer profil özelliklerini burada tanımlayabilirsiniz

    def __str__(self):
        return self.user.username
    
    def to_dict(self):
        return {
            'user': self.user.username,
            'profile_picture': self.profile_picture.url if self.profile_picture else None
            # Diğer profil özelliklerini burada JSON'a dönüştürerek ekleyebilirsiniz
        }

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
    
    @property
    def follower_count(self):
        return self.followers.count()
    
    def blog_count(self):
        return self.blogs.count()

class Draft(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = RichTextField( blank=True, null=True )
    def __str__(self):
        return self.title
    
    @property
    def draft_id(self):
        return self.id

class Blog(models.Model):
    draft = models.ForeignKey(Draft, on_delete=models.CASCADE)
    banner = models.ImageField(upload_to="banners/")
    slug = models.SlugField(default="", blank=True, null=False, unique=True, db_index=True, max_length=250)
    description = models.TextField(max_length=250)
    tags = models.CharField(max_length=500)
    date = models.DateField(auto_now=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='blogs')
    likes = models.ManyToManyField(User, related_name='blog_posts')
    tags = TaggableManager()
    interaction = models.IntegerField(default=0)
    favorite = models.ManyToManyField(User, related_name='favorite_posts', blank=True)
    '''stemmed_content = models.TextField(default="", blank=True, null=True)
    stemmed_title = models.TextField(default="", blank=True, null=True)
    stemmed_tags = models.TextField(default="", blank=True, null=True)
    search_post = SearchVectorField(null=True)
    tags_full = models.CharField(max_length=2550, blank=True, null=True)
    search_author = SearchVectorField(null=True)
    stemmed_author_user = models.TextField(default="", blank=True, null=True)
    stemmed_author_name_surname = models.TextField(default="", blank=True, null=True)'''
    
    def total_likes(self):
        return self.likes.count()

    @classmethod
    def get_most_liked_posts(cls, limit=10):
        return cls.objects.annotate(num_likes=Count('likes')).order_by('-num_likes', '-date')[:limit]

    '''def remove_html_tags(self, text):
        soup = BeautifulSoup(text, 'html.parser')
        return soup.get_text()

    def stemmerTurkish(self, text):
        
        object1 = MyService()
        tokens = text.split()  # Metni boşluklardan ayırarak kelimeleri liste haline getirme

        aa = []

        for token in tokens:
            normalization_input = object1.normalize(token).normalized_input
            analysis_result_token = object1.analyze(token)
            analysis_result_normalization = object1.analyze(normalization_input)

            if normalization_input:
                for a in analysis_result_normalization.results:
                    print(token)
                    print("normalize:" + a.token)
                    best = a.best
                    print(best.pos)
                    if best.lemmas[0] == "UNK":
                        unk_found = False
                        for a_norm in analysis_result_token.results:
                            if a_norm.best.lemmas[0] == "UNK":
                                unk_found = True
                                break
                        if not unk_found:
                            aa.append(a.token.lower())
                            if token.lower() != normalization_input.lower():
                                aa.append(normalization_input)
                        else:
                            aa.append(token.lower())
                    else:
                        aa.append(best.lemmas[0])
        
            
        punctuation = [".", ",", "?", "!", ":", ";", "'", '"', "(", ")", "[", "]", "{", "}", "-", "_", "+", "=", "/", "\\", "|", "<", ">", "@", "#", "$", "%", "^", "&", "*", "~", "`" ]
        result = " ".join(item for item in aa if not any(p in item for p in punctuation))
                

        return result'''

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.draft.title)
            counter = 1
            slug = base_slug
            while Blog.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
    
        '''content_without_html = self.remove_html_tags(self.draft.content)
        self.stemmed_content = self.stemmerTurkish(content_without_html)
        self.stemmed_title = self.stemmerTurkish(self.draft.title)
        self.stemmed_author_user = self.author.user.username
        self.stemmed_author_name_surname = self.author.user.first_name + " " + self.author.user.last_name'''
        super().save(*args, **kwargs)

    '''@receiver(post_save, sender=TaggedItem)
    def handle_taggeditem_save(sender, instance, **kwargs):
        # TaggedItem tablosu güncellendiğinde burası çalışacak
        # İşlemlerinizi burada gerçekleştirin
        # Örneğin, Post modeline etkileyen bir TaggedItem olduğunda ilgili Post'un tags_full alanını güncelleyebilirsiniz

        # Örneğin:
        post = instance.content_object
        
        if isinstance(post, Blog):
            post.update_tags_full()'''
        

    '''def update_search_post(self):
        
        self.search_post = (
            SearchVector('stemmed_title', weight='A', config='simple') +
            SearchVector('stemmed_content', weight='A', config='simple') +
            SearchVector('stemmed_tags', weight='A', config='simple')
        )
        self.search_author = (
            SearchVector('stemmed_author_user', weight='A', config='simple') +
            SearchVector('stemmed_author_name_surname', weight='A', config='simple')
        )


        Blog.objects.filter(id=self.id).update(search_post=self.search_post, search_author=self.search_author)

    def update_tags_full(self):
        tagged_items = TaggedItem.objects.filter(object_id=self.id)
        tag_ids = tagged_items.values_list('tag_id', flat=True)
        tags = Tag.objects.filter(id__in=tag_ids)
        tag_names = ", ".join(tag.name for tag in tags)
        self.tags_full = tag_names
        self.stemmed_tags = self.stemmerTurkish(tag_names)
        super().save(update_fields=['stemmed_tags'])
        super().save(update_fields=['tags_full'])
        self.update_search_post()

    class Meta:
        indexes = [
            GinIndex(fields=['search_post', 'search_author']),
        ]'''

    @property
    def blog_id(self):
        return self.id

class Follow(models.Model):
    '''author_id = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='following')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')'''
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following', null=True)
    following = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='followers', null=True)

    @property
    def follow_id(self):
        return self.id

class Comments(models.Model):
    blog_id = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=500)
    date = models.DateField(auto_now=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    reply = models.ForeignKey("Comments",on_delete=models.DO_NOTHING, blank=True, null=True)

    @property
    def comment_id(self):
        return self.id

# önerilenler için
class UserLikedPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_posts')
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='liked_by')
    tags = models.ManyToManyField(Tag)
    

