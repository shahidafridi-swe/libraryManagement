from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Book, NoticeBoard
from .forms import BookForm, NoticeBoardForm


def books(request):
    books = Book.objects.all()
    notice = NoticeBoard.objects.all()[0]
    context = {
        'books': books,
        'notice': notice
    }
    return render(request, 'library/books.html', context)


def book(request, pk):
    book = Book.objects.get(id=pk)
    context = {
        'book': book
    }
    return render(request, 'library/book.html', context)


@login_required(login_url='login')
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


@login_required(login_url='login')
def updateBook(request, pk):
    book = Book.objects.get(id=pk)
    form = BookForm(instance=book)

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid:
            form.save()
            return redirect('books')
    context = {
        'form': form
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
