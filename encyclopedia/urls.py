from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("createPage", views.createPage, name="createPage"),
    path("create", views.create, name="create"),
    path("search", views.search, name="search"),
    path("<str:wikiContents>", views.wikiContents, name="wikiContents")
]
