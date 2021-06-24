from django.urls import path

from . import views

app_name= "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.view_page, name="view_page"),
    path("s/search", views.search, name="search"),
    path("create", views.create_page, name="create_page"),
    path("edit/<str:entry>", views.edit, name="edit"),
    path("random", views.random, name="random"),
]
