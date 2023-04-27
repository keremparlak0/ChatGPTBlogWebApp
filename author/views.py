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
        if form.is_valid():
            form.save()
            return HttpResponse('New Blog Successfully Added')
    else:
        form = Editor()
        context = {
            'form':form
        }
    return render(request, 'home.html', context)

# site/author/panel
# template: author/panel.html
@login_required()
def panel(request):
    return render(request, "author/panel.html")

# site/author/updatehttps://django-ckeditor.readthedocs.io/en/latest/
# template: author/update.html
@login_required()
def update(request):
    return render(request, "author/update.html")

# site/author/publish
# template: author/publish.html
@login_required()
def publish(request):
    if request.method == "POST":
        form = PublishForm(request.POST, request.FILES)

        if form.is_valid():
            blog = Blog(
                banner = request.FILES["image"],
                title = form.cleaned_data["title"],
                description = form.cleaned_data["description"],
            )
            blog.save()
            return redirect("/author/panel")

    else:
        form = PublishForm()

    return render(request, "author/publish.html", {"form":form})

# site/author/upload
# template: author/library.html
@login_required()
def upload(request):
    form = UploadForm(request.POST, request.FILES)
    if request.method == "POST":
        if form.is_valid():
            image = Library(image = request.FILES["image"])
            image.save()
    else:
        return render(request, "author/library.html", {"form":form})