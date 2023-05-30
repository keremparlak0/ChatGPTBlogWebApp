from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from author.forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from author.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from author.forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from author.models import *
from django.contrib.postgres.search import TrigramSimilarity, TrigramDistance
from django.contrib.postgres.search import SearchQuery, SearchRank
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from django.db.models import FloatField
from django.db.models.functions import Cast
from django.db.models import F, Value
from django.db.models import Q
from django.db import connection
from django.db import models
from .zemberekkk import MyService
from taggit.models import Tag, TaggedItem
from django.db import connections
from django.db.models import Max

def search_tag(request, tag):
    blogs = Blog.objects.filter(tags__name__in=[tag])
    return render(request, 'general/index.html', {"blogs":blogs})

def koklerine_ayir(text):
    object1 = MyService()
    punctuation = [".", ",", "?", "!", ":", ";", "'", '"', "(", ")", "[", "]", "{", "}" ]
    
    analysis_input = text
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
                        aa.append(token)
                else:
                    
                    aa.append(best.lemmas[0].lower())
            
    
    result = " ".join(item for item in aa if not any(p in item for p in punctuation))
    return result

def metni_ara(query1):
    query = """
    SELECT d.id, ab.stemmed_title, ab.stemmed_content, ab.stemmed_tags, ab.stemmed_author_user,
    ts_rank(search_post, websearch_to_tsquery('simple', %s)) +
    ts_rank(search_post, websearch_to_tsquery('simple', %s)) AS rank
    FROM author_blog AS ab
    INNER JOIN author_draft AS d ON ab.draft_id = d.id
    WHERE search_post @@ websearch_to_tsquery('simple', %s)
    OR search_post @@ websearch_to_tsquery('simple', %s)
    """
    search_query = koklerine_ayir(query1)
    print("search_query: " + search_query)
    params = [search_query, search_query, search_query, search_query]
    with connections['default'].cursor() as cursor:
        cursor.execute(query, params)
        results = cursor.fetchall()
        posts = Blog.objects.filter(id__in=[r[0] for r in results])

    return posts

# tag lara göre öneri için en çok bulunan tagları alıyoruz
def get_most_common_tags(num_tags=5):
    most_common_tags = TaggedItem.objects.values('tag_id').annotate(tag_count=Count('tag_id')).order_by('-tag_count')[:num_tags]
    most_common_tag_ids = [tag['tag_id'] for tag in most_common_tags]
    return most_common_tag_ids

# tag lara göre öneri için blogları alıyoruz
def get_posts_with_most_common_tags(num_tags=5):
    most_common_tag_ids = get_most_common_tags(num_tags)
    posts_with_most_common_tags = Blog.objects.filter(tags__id__in=most_common_tag_ids).order_by('-date')
    return posts_with_most_common_tags

def get_recommendations(user, limit=10):
    # Kullanıcının beğendiği gönderileri ve bu gönderilerin etiketlerini al
    liked_posts = UserLikedPost.objects.filter(user=user)
    liked_tags = Tag.objects.filter(userlikedpost__in=liked_posts).distinct()

    # Etiketlere sahip gönderileri çek
    recommended_posts = Blog.objects.filter(tags__in=liked_tags).exclude(liked_by__user=user).distinct().order_by('-interaction')[:limit]

    return recommended_posts

def author_search(text):
    tokens = text.split()

    query = """
    SELECT d.id, ab.author_id, ab.stemmed_author_name_surname,
    ts_rank(search_post, websearch_to_tsquery('simple', %s)) +
    ts_rank(search_post, websearch_to_tsquery('simple', %s)) AS rank
    FROM author_blog AS ab
    INNER JOIN author_draft AS d ON ab.draft_id = d.id
    WHERE search_post @@ websearch_to_tsquery('simple', %s)
    OR search_post @@ websearch_to_tsquery('simple', %s)
    """
    tokens = " ".join(item for item in tokens)
    params = [tokens, tokens, tokens, tokens]
    with connections['default'].cursor() as cursor:
        cursor.execute(query, params)
        results = cursor.fetchall()
        #posts = Blog.objects.filter(id__in=[r[0] for r in results])

    return results


def index(request):
    query1 = request.GET.get('query')
    if query1:
        
        posts = metni_ara(query1)
        posts = posts.order_by('-interaction', '-date')
        
        if posts.count() == 0:
        # yazar araması ve yazara ait yazılar
            author_object = author_search(query1)
            author = Author.objects.filter(id__in=[r[1] for r in author_object])
            author_posts = Blog.objects.filter(author__in=author)
            
            return render(request, 'general/index.html', {'blogs': author_posts})
            
        
        return render(request, 'general/index.html', {'blogs': posts})
        
    if request.method == "GET":
        blogs = Blog.objects.all()
        # blog = recommendation   ~Vural

        # En çok okunan gönderiler
        most_read_posts = Blog.objects.all().order_by('-interaction', '-date')[:10]

        
        # Takipçilerin gönderileri
        if request.user.is_authenticated:
            kullanici = request.user
            author = Author.objects.get(user=kullanici)
            takip_edilenler = Follow.objects.filter(user_id=kullanici)
            takip_edilen_kisiler = Author.objects.filter(id__in=[r.author_id.id for r in takip_edilenler])
            takip_edilenler = Follow.objects.filter(user_id=kullanici)
            author_ids = takip_edilenler.values_list('author_id', flat=True)
            takip_edilen_yazilar = Blog.objects.filter(author__in=author_ids)

            followings = author.following.all()
            posts_for_followings = Blog.objects.filter(author__in=[r.author_id.id for r in followings]).order_by('-interaction', '-date')
            followings = Author.objects.filter(id__in=[r.author_id.id for r in followings]) # author objeleri

            followers = kullanici.followers.all() # user objeleri

            

            # En çok beğenilen gönderiler
            most_liked_posts = Blog.get_most_liked_posts(limit=10)  # En çok beğenilen ve en yeni 5 yazıyı alın

            # Önerilen gönderiler
            recommended_posts = get_recommendations(user=request.user, limit=10)
            
            # taglara göre öneri
            posts_with_most_common_tags = get_posts_with_most_common_tags(num_tags=10)
        
        return render(request, 'general/index.html', {"blogs":blogs})
    
    # arama işlemi 
    elif request.method == "POST":
        #search()    ~Vural
        pass
    else:
        return HttpResponse("Error")

def search(request):
    pass

def recommendation(request): 
    pass


def getProfileBySlug(request, profile_slug):
    profile = Author.objects.get(slug=profile_slug)
    user = request.user
    
    button_name = "Takip Et" 
    if request.user.is_authenticated and Follow.objects.filter(user_id=request.user, author_id=profile).exists():
        button_name = "Takibi Bırak"      

    blogs = {""}
    blogs = Blog.objects.all().filter(author=profile)

    context = {
        'profile': profile,
        'button_name':button_name,
        'blogs':blogs,
    }
    return render(request, 'general/profile.html', context)

def getProfileByID(request, profile_id):
    profile = Author.objects.get(id=profile_id)
    user = request.user   
    button_name = "Takip Et" 
    if request.user.is_authenticated and Follow.objects.filter(user_id=request.user, author_id=profile).exists():
        button_name = "Takibi Bırak"     

    blogs = {""}
    blogs = Blog.objects.all().filter(author=profile)

    context = {
        'profile': profile,
        'button_name':button_name,
        'blogs':blogs,
    }
    return render(request, 'general/profile.html', context)

def getBlogBySlug(request, blog_slug):
    blog = Blog.objects.get(slug=blog_slug)
    blog.interaction += 1
    blog.save()

    button_name = "Takip Et" 
    if request.user.is_authenticated and Follow.objects.filter(user_id=request.user, author_id=blog.author).exists():
        button_name = "Takibi Bırak"     

    form = CommentForm()
    comments = Comments.objects.filter(blog_id=blog)
    context = {
        'blog': blog,
        'form': form,
        'comments':comments,
        'button_name':button_name,
    }
    return render(request, 'general/blog.html', context)

def getBLogById(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    blog.interaction += 1
    blog.save()

    button_name = "Takip Et" 
    if request.user.is_authenticated and Follow.objects.filter(user_id=request.user, author_id=blog.author).exists():
        button_name = "Takibi Bırak"

    form = CommentForm()
    comments = Comments.objects.filter(blog_id=blog)
    context = {
        'blog': blog,
        'form':form,
        'comments':comments,
        'button_name':button_name,
    }
    return render(request, 'general/blog.html', context)

def about(request):
    return render(request,"general/about.html")

def contact(request):
    return render(request, "general/contact.html")

@login_required 
def followAction(request, profile_id):
    profile = Author.objects.get(id=profile_id)

    if request.user.is_authenticated:
        try:
            #if follow exist
            follow = Follow.objects.get(user_id=request.user, author_id=profile)
            follow.delete()
            print("follow deleted")
        except:
            #if follow does not exist
            newfollow = Follow(
            user_id = request.user,
            author_id = profile,
            )
            newfollow.save()
            print("follow created")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect("login")
   
    
@login_required
def like(request, blog_id):
    blog = Blog.objects.get(pk=request.POST.get('blog_id'))
    liked = False
    if blog.likes.filter(id=request.user.id).exists():
        blog.likes.remove(request.user)
        liked = False
    else:
        liked = True
        blog.likes.add(request.user)
    
    return redirect('blogbyslug',blog.slug)



@login_required
def commentAction(request, blog_id=0 ,comment_id=0):
    if request.method == "POST":

        if comment_id==0:
            #create
            blog = Blog.objects.get(pk=blog_id)
            comment = Comments(
                blog_id = blog,
                user_id = request.user,
                message = request.POST["message"]
            )
            comment.save()

        elif blog_id==0:
            #delete
            comment = get_object_or_404(Comments, pk=comment_id)
            if request.user == comment.user_id:
                comment.delete()   
        # else:
        #     #update
        #     pass

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))