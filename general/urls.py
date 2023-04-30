from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('index', views.index, name="index"),
    path('profile/<slug:profile_id>', views.getProfileByID, name="profilebyid"),
    path('profile/<slug:profile_slug>', views.getProfileBySlug, name="profilebyslug"),
    path('blog/<int:blog_id>', views.getBLogById, name="blogbyid"),
    path('blog/<slug:blog_slug>',views.getBlogBySlug, name="blogbyslug"),
]
