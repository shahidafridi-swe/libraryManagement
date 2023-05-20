from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Book, BookIssue, NoticeBoard
from .forms import BookForm, NoticeBoardForm, BookIssueForm
from django.contrib import messages
from datetime import date
from .utils import bookSearch, issuedBookSearch, paginateBooks,paginateIssuedBooks

def books(request):
    books, search_query = bookSearch(request)
    issued_books = BookIssue.objects.values_list('book_id', flat=True)
    notice = NoticeBoard.objects.all()[0]
    books, custom_range, paginator = paginateBooks(request, books, 1)
    context = {
        'books': books,
        'issued_books': issued_books,
        'notice': notice,
        'search_query':search_query,
        'custom_range':custom_range,
        'paginator':paginator
    }
    return render(request, 'library/books.html', context)


def book(request, pk):
    book = Book.objects.get(id=pk)
    issued_book = BookIssue.objects.filter(
        book=book, return_date__gte=date.today()).first()
    is_issued = issued_book is not None
    context = {
        'book': book,
        'is_issued': is_issued,
        'issued_book': issued_book
    }
    return render(request, 'library/book.html', context)


@login_required(login_url='login')
def createBook(request):
    page = 'create-book'
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid:
            form.save()
            return redirect('books')
    context = {
        'page': page,
        'form': form
    }
    return render(request, 'library/book-form.html', context)


@login_required(login_url='login')
def updateBook(request, pk):
    page = 'update-book'
    book = Book.objects.get(id=pk)
    form = BookForm(instance=book)

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid:
            form.save()
            return redirect('books')
    context = {
        'page': page,
        'form': form,
        'book': book
    }
    return render(request, 'library/book-form.html', context)


@login_required(login_url='login')
def deleteBook(request, pk):
    book = Book.objects.get(id=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('books')
    context = {
        'book': book
    }
    return render(request, 'library/book-delete.html', context)


@login_required(login_url='login')
def noticeUpdate(request, pk):
    notice = NoticeBoard.objects.get(id=pk)
    form = NoticeBoardForm(instance=notice)

    if request.method == 'POST':
        form = NoticeBoardForm(request.POST, instance=notice)
        if form.is_valid:
            form.save()
            return redirect('books')

    context = {
        'form': form,
        'notice': notice
    }
    return render(request, 'library/notice-form.html', context)


@login_required(login_url='login')
def issueBook(request, pk):
    book = Book.objects.get(id=pk)
    librarian = request.user.librarian
    form = BookIssueForm()
    if request.method == 'POST':
        form = BookIssueForm(request.POST)
        if form.is_valid:
            issue = form.save(commit=False)
            issue.book = book
            issue.librarian = librarian
            issue.save()
            messages.success(request, "Book issue has successfull!")
            return redirect('issued-books')
      
    context = {
        'book': book,
        'librarian': librarian,
        'form': form
    }
    return render(request, 'library/book_issue_form.html', context)


@login_required(login_url='login')
def issuedBooks(request):
    books, search_query = issuedBookSearch(request)
    books, custom_range = paginateIssuedBooks(request, books, 1)
    context = {
        'books': books,
        'search_query':search_query,
        'custom_range':custom_range
    }
    return render(request, 'library/issued_books.html', context)


@login_required(login_url='login')
def issuedBookDetails(request, pk):
    book = BookIssue.objects.get(id=pk)
    context = {
        'book': book
    }
    return render(request, 'library/issued_book_details.html', context)


@login_required(login_url='login')
def returnBook(request, pk):
    book = BookIssue.objects.get(id=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('issued-books')
    context = {
        'book': book
    }
    return render(request, 'library/return_book.html', context)
