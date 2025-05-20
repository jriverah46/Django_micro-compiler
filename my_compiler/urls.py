
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('editor/', views.editor, name='editor'),
    path('compile/', views.compile, name='compile'),
    path('execute/', views.execute, name='execute'),
    path('tokens/', views.tokens, name='tokens'),
    path('save/', views.save_file, name='save_file'),
    path('files/', views.files_list, name='files'),
    path('delete/<int:file_id>/', views.delete_file, name='delete_file'),
    path('open/<int:file_id>/', views.open_file, name='open_file'),
    path('new_file/', views.new_file, name='new_file'),
]