from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index),
    path('index', views.index, name="index"),
    path('profile/<int:profile_id>', views.getProfileByID, name="profile"),
    path('profile/<str:profile_slug>', views.getProfileBySlug, name="profile"),
    path('blog/<int:blog_id>', views.getBLogById, name="blog"),
    path('blog/<str:blog_slug>',views.getBlogBySlug, name="blog"),
    path('blog/<int:blog_id>/comment', views.comment, name='comment'),
    path('blog/<int:blog_id>/like', views.like, name='like'),
    path('followers_count', views.followers_count, name='followers_count'),
    path('delete_comment/<int:comment_id>', views.delete_comment, name='delete_comment'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


