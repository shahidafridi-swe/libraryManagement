from django.urls import path

from . import views

urlpatterns = [
    path("", views.books, name="books"),
    path("book/<str:pk>/", views.book, name="book"),
    path("create-book/", views.createBook, name="create-book"),
    path("update-book/<str:pk>/", views.updateBook, name="update-book"),
    path("delete-book/<str:pk>/", views.deleteBook, name="delete-book"),
    path("update-notice/<str:pk>/", views.noticeUpdate, name="notice-update"),
    path("issue-book/<str:pk>/", views.issueBook, name="issue-book"),
    path("issued-books/", views.issuedBooks, name='issued-books'),
    path("issued-book-details/<str:pk>/",
         views.issuedBookDetails, name='issued-book-details'),
    path("return-book/<str:pk>/", views.returnBook, name="return-book"),

]
