from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Book, BookIssue, NoticeBoard
from .forms import BookForm, NoticeBoardForm,BookIssueForm
from django.contrib import messages

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

def issueBook(request,pk):
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
            return redirect('books')
        
    context={
      'book':book,
      'librarian':librarian,
      'form':form
    }
    return render(request, 'library/book_issue_form.html',context)

def issuedBooks(request):
    books = BookIssue.objects.all()
    context = {
        'books':books
    }
    return render(request, 'library/issued_books.html',context)

def issuedBookDetails(request,pk):
    book = BookIssue.objects.get(id=pk)
    context = {
        'book': book
    }
    return render(request, 'library/issued_book_details.html', context)

def returnBook(request,pk):
    book = BookIssue.objects.get(id=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('issued-books')
    context = {
        'book': book
    }
    return render(request, 'library/return_book.html', context)