from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("search", views.search, name="search"),
    path("edit/<str:edit>", views.update, name="update"),
    path("<str:wikiContents>", views.wikiContents, name="wikiContents")
]
