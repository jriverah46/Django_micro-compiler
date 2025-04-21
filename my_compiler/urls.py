
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home,name='home'),
    path('editor/', views.editor,name='editor'),
    path('delete_file/<int:file_id>', views.delete_file,name='delete_file'),
    path('open_file/<int:file_id>', views.open_file,name='open_file'),
    path("compile/",views.compile,name="compile"),
    path("tokens/",views.tokens,name="tokens"),
    path("save_file/",views.save_file,name="save_file"),
    path("files/",views.files_list,name="files"),
    path("new_file/",views.new_file,name="new_file")
    
]