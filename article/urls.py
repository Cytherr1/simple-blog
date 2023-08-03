from django.contrib import admin
from django.urls import path, include

from . import views

app_name = "article"

urlpatterns = [
    path('dashboard/', views.dashboard, name = "dashboard"),
    path('create/', views.create, name = "create"),
    path('article/<int:id>', views.detail, name = "detail"),
    path('edit/<int:id>', views.edit, name = "edit"),
    path('delete/<int:id>', views.deleteArticle, name = "deleteArticle"),
    path('', views.articles, name = "articles"),
    path('comment/<int:id>', views.addComment, name = "addComment"),
]