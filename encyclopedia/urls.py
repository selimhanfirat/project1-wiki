from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new_page", views.new_page, name="new_page"),
    path('<str:article_name>/', views.article, name='article'),
    path('random', views.random, name = "random")
]
