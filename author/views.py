from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
import openai
import requests
from author.forms import *
from author.models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# site/author/editor
# template: author/editor.html   #ckeditor
@login_required()
def newDraft(request):
    author = Author.objects.get(user = request.user)
    draft = Draft(content = "", title="", author = author)
    draft.save()

    return redirect("panel")

# site/author/editor/<draft_id>
# template: author/editor.html   #ckeditor
@login_required()
def editor(request, draft_id):
    draft = get_object_or_404(Draft, pk=draft_id)
    author = Author.objects.get(user = request.user)

    # if author own this draft
    if draft.author == author:
        if request.method == 'POST':
            form = Editor(request.POST, instance=draft)
            form.save()
            return render(request, 'author/editor.html', {"form":form, "draft":draft})
        else:
            form = Editor(instance=draft)
            return render(request, 'author/editor.html', {"form":form, "draft":draft})
    else:
        return HttpResponse("Yetkisiz erişim")

    
@login_required
def delDraft(request, draft_id):
    draft = get_object_or_404(Draft, pk=draft_id)
    author = Author.objects.get(user = request.user)

    # if author own this draft
    if draft.author == author:
        if request.method == 'POST':
            draft.delete()
            return redirect("panel")
        else:
            return render(request, "author/confirm.html", {"contex":draft.title})
    else:
        return HttpResponse("Yetkisiz erişim")

def generate_text2(prompt):
    openai.api_key = "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"
    URL = "https://api.openai.com/v1/chat/completions"
    message = prompt
    payload = {
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": f" {message} hakkında hakkında en fazla 15 kelimelik bir blog yazısı istiyorum. Profesyonel bir yazarın yazdığı gibi yazın."}], 
    "temperature" : 1.0,
    "top_p":1.0,
    "n" : 5,
    
    "presence_penalty":0,
    "frequency_penalty":0,
    }

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai.api_key}"
    }

    response = requests.post(URL, headers=headers, json=payload, stream=False)
    reply = response.json()
    
    return reply

def generate_text(prompt):
    URL = "https://api.openai.com/v1/chat/completions"
    message = prompt
    payload = {
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": f" Metnin etiketlerini alarak numaralı şekilde listelemek istiyorum. Lütfen aşağıdaki metin kutusuna bir metin girin: Metin: {message}. etiketleri '#' işareti ile ayrılarak yazın"}],
    "messages": [{"role": "user", "content": f"Please provide a text input for which you would like me to generate tags. Once you provide the input, I will generate #tag1, #tag2 formatted tags for it. Please enter your input below: {message}."}], 
    "temperature" : 1.0,
    "top_p":1.0,
    "n" : 5,
    
    "presence_penalty":0,
    "frequency_penalty":0,
    }

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai.api_key}"
    }

    response = requests.post(URL, headers=headers, json=payload, stream=False)
    reply = response.json()
    
    return reply

# site/author/publish/<draft_id>
# template: author/publish.html
@login_required()
def publish(request, draft_id):
    record = get_object_or_404(Draft, pk=draft_id)
    author = Author.objects.get(user = request.user)

    openai.api_key = "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"
    message = generate_text(record.content)
    print(message)
    try:
        data = message["choices"]
        content_list = [item['message']['content'] for item in data]
        content_list = content_list[0].split("#")[1:4]
    except:
        content_list = None
    
    try:
        blog = Blog.objects.get(draft=record)
    except Blog.DoesNotExist:
        blog = None

    # if author own this draft
    if record.author == author:
        if request.method == "POST":
            form = PublishForm(request.POST, request.FILES)
            if form.is_valid():
                if blog:
                    blog.draft = record
                    blog.banner = request.FILES["banner"]
                    blog.description = form.cleaned_data["description"]
                    blog.save()
                    blog.tags.clear()
                    blog.tags.add(*form.cleaned_data["tags"])
                    return redirect("panel")
                else:
                    blog = Blog(
                        author = author,
                        draft = record,
                        banner = request.FILES["banner"],
                        description = form.cleaned_data["description"],
                    )
                    blog.save()
                    blog.tags.add(*form.cleaned_data["tags"])
                    return redirect("panel")
        else:
            if blog:
                tags = ",".join([tag.name for tag in blog.tags.all()])
                form = PublishForm(instance=blog, initial={"tags":tags})
            else:
                if content_list:
                    tags = ",".join(content_list)
                else:
                    tags = None
                form = PublishForm(initial={"tags":tags})
        return render(request, "author/publish.html", {"form":form})
    else:
        return HttpResponse("Yetkisiz erişim")


# site/author/panel
# template: author/panel.html
@login_required()
def panel(request):
    author = is_author(request)
    if(author):
        blogs = {""}
        blogs = Draft.objects.all().filter(author=author)
        
        return render(request, "author/panel.html", {"blogs":blogs, "profile":author})
    else:
        return redirect("update")

# site/author/update/
# template: author/update.html
@login_required()
def update(request, message=""):
    try:
        author = Author.objects.get(user = request.user)
    except Author.DoesNotExist:
        author = None

    if request.method == 'POST':
        form = UpdateForm(request.POST, request.FILES)
        if form.is_valid():
            if author:
                author.about = form.cleaned_data["about"]
                author.contact = form.cleaned_data["contact"]
                author.birthday = form.cleaned_data["birthday"]
                if request.FILES.get("picture"):
                    author.picture = request.FILES["picture"]
                author.save()
                user_profile = UserProfile.objects.get(user=request.user)
                user_profile.profile_picture = author.picture
                user_profile.save()
            else:

                author = Author(
                    user = request.user,
                    about = form.cleaned_data["about"],
                    contact = form.cleaned_data["contact"],
                    birthday = form.cleaned_data["birthday"],
                    picture = request.FILES["picture"],
                    )
                author.save() 
                user_profile = UserProfile.objects.get(user=request.user)
                user_profile.profile_picture = author.picture
                user_profile.save()
            

            return redirect("panel")
        else:
            return HttpResponse("form geçerli değil")
    else:
        if author:
            form = UpdateForm(instance=author)
        else:
            form = UpdateForm()
        context = {
            'message':message,
            'form':form,
        }
        return render(request, 'author/update.html', context)

# site/author/upload
# template: author/library.html
# @login_required()
# def upload(request):
#     form = UploadForm(request.POST, request.FILES)
#     if request.method == "POST":
#         if form.is_valid():
#             image = Library(image = request.FILES["image"])
#             image.save()
#     else:
#         return render(request, "author/library.html", {"form":form})

def is_author(request):
    user = request.user
    try:
        author = Author.objects.get(user_id=user)
        return author
    except:
        return False


def yazmayabasla(request):
    try:
        author = Author.objects.get(user = request.user)
        draft = Draft(content = "", title="", author = author)
        draft.save()

        return redirect("editor", draft_id=draft.id)
    except:
        return redirect("update")
    

@csrf_exempt
def publishajax(request):
    user = request.user
    author = Author.objects.get(user_id=user)
    if request.method == 'POST':
        # Formdan gelen verileri al
        title = request.POST.get('title')
        content = request.POST.get('content')
        draft_id = request.POST.get('draft_id')
        if content == "" or title == "":
            return JsonResponse({'success': False, 'message': 'Başlık veya içerik boş olamaz'}, status=400)
        print(title)    
        print(content)
        try:
            draft = Draft.objects.get(id=draft_id)
            draft.title = title
            draft.content = content
            draft.save()
        except:
            draft = Draft.objects.create(author=author, title=title, content=content)
        draft.save()

        
        


        # Başarılı yanıt döndür
        return JsonResponse({'success': True, 'draft_id': draft.id})
    
    # Hatalı istek durumunda hata yanıtı döndür
    return JsonResponse({'success': False, 'message': 'Geçersiz istek'}, status=400)

@csrf_exempt
def aboutajax(request):
    user = request.user
    author = Author.objects.get(user_id=user)
    if request.method == 'POST':
        # Formdan gelen verileri al
        about = request.POST.get('about')
        print(about)
        if about == "":
            return JsonResponse({'success': False, 'message': 'Başlık veya içerik boş olamaz'}, status=400)
        print(about)    
        
        try:
            author.about = about
            author.save()
        except:
            return JsonResponse({'success': False, 'message': 'Hata oluştu'}, status=400)
        
        


        # Başarılı yanıt döndür
        return JsonResponse({'success': True, 'author_id': author.id, 'about': about})
    
    # Hatalı istek durumunda hata yanıtı döndür
    return JsonResponse({'success': False, 'message': 'Geçersiz istek'}, status=400)


@csrf_exempt
def getsuggestions(request):
    if request.method == 'POST':
        # Formdan gelen verileri al
        title = request.POST.get('title')
        
        suggest = generate_text2(title)
        
        reply = suggest['choices'][0]["message"]["content"]
        print(reply)


        # Başarılı yanıt döndür
        return JsonResponse({'success': True, 'suggest': reply})
    
    # Hatalı istek durumunda hata yanıtı döndür
    return JsonResponse({'success': False, 'message': 'Geçersiz istek'}, status=400)