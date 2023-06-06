from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

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


# site/author/publish/<draft_id>
# template: author/publish.html
@login_required()
def publish(request, draft_id):
    record = get_object_or_404(Draft, pk=draft_id)
    author = Author.objects.get(user = request.user)

    # if author own this draft
    if record.author == author:
        if request.method == "POST":
            form = PublishForm(request.POST, request.FILES)
            if form.is_valid():
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
            form = PublishForm()

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
    if request.method == 'POST':
        form = UpdateForm(request.POST, request.FILES)
        if form.is_valid():
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
        print("POST geldiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
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
