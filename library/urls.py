from django.urls import path

from . import views

urlpatterns = [
    path("", views.books, name="books"),
    path("book/<str:pk>/", views.book, name="book"),
    path("book/create-book", views.createBook, name="create-book"),
    path("update-book/<str:pk>/", views.updateBook, name="update-book"),
    path("delete-book/<str:pk>/", views.deleteBook, name="delete-book"),

]