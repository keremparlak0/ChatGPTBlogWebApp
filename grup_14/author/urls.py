from django.urls import include, path
from . import views
from django.conf.urls.static import static
from django.conf import settings
import general.views


urlpatterns = [
    path('', general.views.index, name='index'),
    path('panel', views.panel, name='panel'),
    path('update', views.update, name='update'),
    path('publish', views.publish, name='publish'),
    path('upload', views.upload, name='upload'),
    path('editor', views.editor, name='editor'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

