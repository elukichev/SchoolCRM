from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('projects/', views.project_list),
    path('projects/<slug:slug>/', views.project_details)
]