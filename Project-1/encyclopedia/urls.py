from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.get_page, name="get_page"),
    path("search/", views.search, name="search"),
    path("create/", views.create_page, name="create_page"),
    path("edit/", views.edit_page, name="edit_page"),
    path("save-edit/", views.save_edit, name="save_edit"),
    path("random/", views.random_page, name="random_page"),
]
