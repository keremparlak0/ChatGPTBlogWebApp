from django.urls import include, path
from . import views
from django.conf.urls.static import static
from django.conf import settings
import general.views


urlpatterns = [
    path('', general.views.index, name='index'),
    path('panel/', views.panel, name='panel'),
    path('update', views.update, name='update'),
    path('publish/<int:draft_id>', views.publish, name='publish'),
    path('upload', views.upload, name='upload'),
    path('editor', views.editor, name='editor'),
    path('edit_draft/<int:draft_id>', views.edit_draft, name='edit-draft'),
    path('myblogs', views.myblogs, name='myblogs'),
    path('update/<int:blog_id>', views.update_blog, name='update-blog'),
    path('update/draft/<slug:blog_slug>', views.update_draft, name='update-draft'),
    path('publish2', views.publish2, name='publish2'),
    path('update/blog/<slug:blog_slug>', views.update_blog2, name='update-blog2'),
    path('publish3/<int:draft_id>', views.publish3, name='publish3'),
    path('publish4', views.publish4, name="publish4"),
    path('delete/post/<int:blog_id>', views.delete_post, name='delete'),
    path('updateauthor', views.update_author, name='updateauthor'),
    path('updateauthor2', views.update_author2, name='updateauthor2'),
    path('updateuser', views.update_user, name='updateuser'),
    path('updateuser2', views.update_user2, name='updateuser2'),
    path('editor/<slug:draft_slug>', views.editor2, name='editor2'),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

