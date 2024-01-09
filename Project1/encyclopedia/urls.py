from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry_name>", views.entry_view, name="entry_detail"),
    path("random", views.random_page, name="random"),
    path("search", views.search, name="search"),
    path("newpage", views.newpage, name="newpage"),
    path("wiki/<str:entry_name>/edit", views.editpage, name="editpage")
]
