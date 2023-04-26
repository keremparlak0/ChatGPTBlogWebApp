from django.urls import path
from . import views
import general.views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("", general.views.index, name="index"),
    path("login", views.login_request, name="login"),
    path("register", views.register_request, name="register"),
    path("logout", views.logout_request, name="logout"),
    path("update", views.update_request, name="update"),
    path("update/author", views.update_author_request, name="update-author"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

