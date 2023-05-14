from django.shortcuts import render, redirect
from .models import Book
from .forms import BookForm


def books(request):
    books = Book.objects.all()
    context = {
        'books': books
    }
    return render(request, 'library/books.html', context)


def book(request, pk):
    book = Book.objects.get(id=pk)
    context = {
        'book': book
    }
    return render(request, 'library/book.html', context)


def createBook(request):
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid:
            form.save()
            return redirect('books')
    context = {
        'form': form
    }
    return render(request, 'library/book-form.html', context)


def updateBook(request, pk):
    book = Book.objects.get(id=pk)
    form = BookForm(instance=book)

    if request.method == 'POST':
        form = BookForm(request.POST,request.FILES, instance=book)
        if form.is_valid:
            form.save()
            return redirect('books')
    context = {
        'form': form
    }
    return render(request, 'library/book-form.html', context)


def deleteBook(request, pk):
    book = Book.objects.get(id=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('books')
    context = {
        'book': book
    }
    return render(request, 'library/book-delete.html', context)