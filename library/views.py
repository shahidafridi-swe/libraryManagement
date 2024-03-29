from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Book, BookIssue, NoticeBoard
from .forms import BookForm, NoticeBoardForm, BookIssueForm
from django.contrib import messages
from datetime import date, datetime
from .utils import bookSearch, issuedBookSearch, paginateBooks, paginateIssuedBooks


def home(request):
    books, search_query = bookSearch(request)
    issued_books = BookIssue.objects.values_list('book_id', flat=True)
    notice = NoticeBoard.objects.all()[0]
    books, custom_range, paginator = paginateBooks(request, books, 10)
    context = {
        'books': books,
        'issued_books': issued_books,
        'notice': notice,
        'search_query': search_query,
        'custom_range': custom_range,
        'paginator': paginator,
     
    }
    return render(request, 'library/home.html', context)


def books(request):
    books, search_query = bookSearch(request)
    issued_books = BookIssue.objects.values_list('book_id', flat=True)
    notice = NoticeBoard.objects.all()[0]
    books, custom_range, paginator = paginateBooks(request, books, 10)
    context = {
        'books': books,
        'issued_books': issued_books,
        'notice': notice,
        'search_query': search_query,
        'custom_range': custom_range,
        'paginator': paginator
    }
    return render(request, 'library/books.html', context)


def book(request, pk):
    book = Book.objects.get(id=pk)
    issued_book = BookIssue.objects.filter(
        book=book)
    context = {
        'book': book,
        'issued_book': issued_book
    }
    return render(request, 'library/book.html', context)


@login_required(login_url='login')
def createBook(request):
    page = 'create-book'
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        try:
            if form.is_valid:
                form.save()
                return redirect('books')
        except:
            messages.error(
                request, 'An error has occurred during book add')

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
        try:
            if form.is_valid:
                form.save()
                return redirect('books')
        except:
            messages.error(
                request, 'An error has occurred during book add')
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
        try:
            if form.is_valid:
                issue = form.save(commit=False)
                issue.book = book
                issue.librarian = librarian
                issue.save()
                emailSubject = 'Book Issue From Library of Presidency University'
                emailBody = f"{issue.person_name} (ID: {issue.person_id}), Your requested book has successfully issued. \n \n Issue Details: \n Book Title: {issue.book.title} \n Author: {issue.book.author} \n Accession Number: {issue.book.accession_number} \n Issue Date: {issue.issued_date} \n Return Date: {issue.return_date} \n \n Issued by: {issue.librarian.name} (ID: {issue.librarian.institute_id}) \n PRESIDENCY UNIVERSITY "
                send_mail(
                    emailSubject,
                    emailBody,
                    settings.EMAIL_HOST_USER,
                    [issue.person_email],
                    fail_silently=False
                )

                messages.success(request, "Book issue has successfull!")
                return redirect('issued-books')
        except:
            messages.error(
                request, 'An error has occurred during book add')
    context = {
        'book': book,
        'librarian': librarian,
        'form': form
    }
    return render(request, 'library/book_issue_form.html', context)


@login_required(login_url='login')
def issuedBooks(request):
    books, search_query = issuedBookSearch(request)
    current_date = datetime.now().date()
    books, custom_range = paginateIssuedBooks(request, books, 10)
    context = {
        'books': books,
        'search_query': search_query,
        'custom_range': custom_range,
        'current_date': current_date
    }
    # Send email for expired return dates
    for book in books:
        if book.return_date < current_date and not book.email_sent:
            subject = 'Book Return Reminder'
            message = f'Dear {book.person_name},\n\n' \
                f"This is a reminder that the return date for the book '{book.book.title}' " \
                f"has expired. Please return the book as soon as possible.\n\n" \
                f"Thank you.\n\n" \
                f"Library Management"
            from_email = settings.EMAIL_HOST_USER
            to_email = [book.person_email]
            send_mail(subject, message, from_email,
                      to_email,  fail_silently=False)

            # send_mail_to_person(book)
            book.email_sent = True
            book.save()
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
    current_date = datetime.now().date()
    if request.method == 'POST':
        emailSubject = 'Issued Book Return To Library of Presidency University'
        emailBody = f"{book.person_name}, Your issued book has successfully returned.\n You have returned at: {current_date} \n \n Issue Details: \n Book Title: {book.book.title} \n Author: {book.book.author} \n Accession Number: {book.book.accession_number} \n Issue Date: {book.issued_date} \n Return Date: {book.return_date} \n \n Issued by: {book.librarian.name} (ID: {book.librarian.institute_id}) \n PRESIDENCY UNIVERSITY "
        send_mail(
            emailSubject,
            emailBody,
            settings.EMAIL_HOST_USER,
            [book.person_email],
            fail_silently=False
        )
        book.delete()
        return redirect('issued-books')
    context = {
        'book': book
    }
    return render(request, 'library/return_book.html', context)
