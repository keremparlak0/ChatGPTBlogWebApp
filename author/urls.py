from django.urls import include, path

from grup_14 import settings
from . import views

urlpatterns = [
    path('panel/', views.panel, name="panel"),
    path('update/', views.update, name="update"),
    #path('upload/', views.upload),
    path('editor/<int:draft_id>', views.editor, name="editor"),             # edit draft
    path('editor/delete/<int:draft_id>', views.delDraft, name="delDraft"),  # delete draft
    path('editor/new/', views.newDraft, name="newDraft"),                   # create draft
    path('publish/<int:draft_id>', views.publish, name="publishDraft"),     # publish draft
    path('yazmayabasla/', views.yazmayabasla, name="yazmayabasla"),         # create draft's content
]
