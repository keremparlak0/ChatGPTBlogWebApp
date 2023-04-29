from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from author.forms import *
from author.models import *


# Create your views here.

# session kontrolü yapılacak

# site/author/editor
# template: author/editor.html   #ckeditor
@login_required()
def editor(request):
    if request.method == 'POST':
        form = Editor(request.POST)

        author = Author.objects.get(user = request.user)

        if form.is_valid():
            draft = Draft(content=form.cleaned_data["content"], author= author)
            draft.save() 
        return HttpResponse("Yazı oluşturuldu")
    else:
        form = Editor()
        context = {
            'form':form
        }
        return render(request, 'author/editor.html', context)



# site/author/panel
# template: author/panel.html
@login_required()
def panel(request):
    author = Author.objects.get(user = request.user)
    print(author)
    blogs = Blog.objects.get(author=author)
    blogs = blogs.title
    print(blogs)

    return render(request, "author/panel.html", {"blogs":blogs})

# site/author/update/
# template: author/update.html
@login_required()
def update(request):
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
            return HttpResponse("yazar başarıyla oluşturuldu")
    else:
        form = UpdateForm()
        context = {
            'form':form
        }
    return render(request, 'author/update.html', context)



# site/author/publish/?draft=draft_id
# template: author/publish.html
@login_required()
def publish(request):
    draft = request.GET.get("draft", None)
    record = Draft.objects.get(id=draft)
    author = Author.objects.get(user = request.user)

    # if author own this draft
    if record.author == author:
        if request.method == "POST":
            form = PublishForm(request.POST, request.FILES)
            if form.is_valid():
                blog = Blog(
                    author = author,
                    draft = record,
                    tags = form.cleaned_data["tags"],
                    banner = request.FILES["banner"],
                    title = form.cleaned_data["title"],
                    description = form.cleaned_data["description"],
                )
                blog.save()
                return HttpResponse("blog başaryla oluşturuldu")
        else:
            form = PublishForm()

        return render(request, "author/publish.html", {"form":form})
    else:
        return HttpResponse("Yetkisiz erişim")



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