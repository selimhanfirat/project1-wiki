from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new_page", views.new_page, name="new_page"),
    path('random', views.random, name="random"),
    path('search', views.search, name="search"),
    path('edit_article/<str:article_name>/', views.edit_article, name='edit_article'),
    path('save_edited_article/<str:article_name>/', views.save_edited_article, name='save_edited_article'),
    path('<str:article_name>/', views.article, name='article'),
]
