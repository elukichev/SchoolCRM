from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.index, name='index'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/create', views.project_create, name='project_create'),
    path('projects/<int:project_id>/', views.project_details, name='project_details'),
    path('projects/<int:project_id>/task-create', views.task_create, name='task_create'),
    path('projects/<int:project_id>/add-executor', views.add_project_executor, name='add_project_executor'),
]