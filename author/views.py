from django.shortcuts import redirect, render

from author.forms import PublishForm, UploadForm
from author.models import Library

# Create your views here.
def editor(request):
    return render(request, 'editor.html')

def panel(request):
    return render(request, "panel.html")

def update(request):
    return render(request, "update.html")

def publish(request):
    if request.method == "POST":
        form = PublishForm()

        if form.is_valid():
            blog = Blog(title=form.cleaned_data["title"], 
                        description=form.cleaned_data["description"],
                        ...
                        )
            blog.save()
            return redirect("/author/panel")

    else:
        form = PublishForm()

    return render(request, "publish.html", {"form":form})

def upload(request):
    form = UploadForm(request.POST, request.FILES)
    if request.method == "POST":
        if form.is_valid():
            image = Library(image = request.FILES["image"])
            image.save()
    else:
        return render(request, "library.html", {"form":form})