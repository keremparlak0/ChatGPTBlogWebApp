from django.shortcuts import redirect, render

from author.forms import PublishForm, UploadForm
from author.models import *

# Create your views here.

# site/author/editor
# template: author/editor.html   #ckeditor
def editor(request):
    return render(request, 'editor.html')

# site/author/panel
# template: author/panel.html
def panel(request):
    return render(request, "panel.html")

# site/author/update
# template: author/update.html
def update(request):
    return render(request, "update.html")

# site/author/publish
# template: author/publish.html
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

    return render(request, "publish.html", {"form":form})

# site/author/upload
# template: author/library.html
def upload(request):
    form = UploadForm(request.POST, request.FILES)
    if request.method == "POST":
        if form.is_valid():
            image = Library(image = request.FILES["image"])
            image.save()
    else:
        return render(request, "library.html", {"form":form})