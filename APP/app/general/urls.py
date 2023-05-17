from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('index', views.index, name="index"),
    path('profile/<int:profile_id>', views.getProfileByID, name="profilebyid"),
    path('profile/<slug:profile_slug>', views.getProfileBySlug, name="profilebyslug"),
    path('blog/<int:blog_id>', views.getBLogById, name="blogbyid"),
    path('blog/<int:blog_id>/like', views.like, name='like'),
    path('blog/<slug:blog_slug>',views.getBlogBySlug, name="blogbyslug"),

    path('blog/<int:blog_id>/comment', views.comment, name='comment'),
    path('blog/delete_comment/<int:comment_id>', views.delete_comment, name='delete_comment'),
    #path('blog/edit_comment/<int:comment_id>', views.edit_comment, name='delete_comment'),

]
