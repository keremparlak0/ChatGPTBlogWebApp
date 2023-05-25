from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('index', views.index, name="index"),
    path('search',views.search, name="search"),
    path('about',views.about, name="about"),
    path('contact',views.contact, name="contact"),
    path('profile/<int:profile_id>', views.getProfileByID, name="profilebyid"),
    path('profile/<slug:profile_slug>', views.getProfileBySlug, name="profilebyslug"),
    path('profile/<int:profile_id>/follow', views.followAction, name="followAction"),
    path('blog/<int:blog_id>', views.getBLogById, name="blogbyid"),
    path('blog/<int:blog_id>/like', views.like, name='likebyid'),
    path('blog/<slug:blog_slug>',views.getBlogBySlug, name="blogbyslug"),
     path('blog/<int:blog_slug>/like', views.like, name='likebyslug'),

    path('blog/<int:blog_id>/comment/<int:comment_id>', views.commentAction, name='commentAction'),
    path('blog/<int:blog_id>/comment/', views.commentAction, name='commentAction'),
]
