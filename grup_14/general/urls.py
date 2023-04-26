from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index),
    path('index', views.index, name="index"),
    path('profile/<int:profile_id>', views.getProfileByID),
    path('profile/<str:profile_slug>', views.getProfileBySlug),
    path('blog/<int:blog_id>', views.getBLogById),
    path('blog/<str:blog_slug>',views.getBlogBySlug),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


