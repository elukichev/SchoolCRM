from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.index, name='index'),
    path('projects/', views.project_list),
    path('projects/<slug:slug>/', views.project_details)
]