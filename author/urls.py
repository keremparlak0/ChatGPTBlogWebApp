from django.urls import include, path
from . import views

urlpatterns = [
    path('panel', views.panel),
    path('update', views.update),
    path('publish', views.publish),
    path('upload', views.upload),
    path('editor', views.editor, name='editor'),
]