from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.index, name='index'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/create', views.project_create, name='project_create'),
    path('projects/create', views.project_create, name='project_create'),
    path('projects/<int:project_id>/edit', views.project_edit, name='project_edit'),
    path('projects/<int:project_id>/', views.project_details, name='project_details'),
    path('projects/<int:project_id>/task-create', views.task_create, name='task_create'),
    path('projects/<int:project_id>/add-executor', views.add_project_executor, name='add_project_executor'),
    path('projects/<int:project_id>/task/<int:task_id>', views.task_details, name='task_details'),
    path('projects/<int:project_id>/task/<int:task_id>/subtusk-create', views.subtask_create, name='subtask_create'),
    path(
        'projects/<int:project_id>/task/<int:task_id>/done/<int:subtask_id>',
        views.subtask_done,
        name='subtask_done'
    ),
    path(
        'projects/<int:project_id>/task/<int:task_id>/delete/<int:subtask_id>',
        views.subtask_delete,
        name='subtask_delete'
    ),
    path(
        'projects/<int:project_id>/task/delete/<int:task_id>',
        views.task_delete,
        name='task_delete'
    ),

]