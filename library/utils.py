from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q 
from .models import Book, BookIssue

def bookSearch(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
      
    books = Book.objects.filter(
        Q(title__icontains=search_query) |
        Q(author__icontains=search_query) |
        Q(publication__icontains=search_query) |
        Q(accession_number__icontains=search_query) 

    )

    return books, search_query


def issuedBookSearch(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    
    title = Book.objects.filter(title__icontains=search_query)

    books = BookIssue.objects.filter(
        Q(person_name__icontains=search_query) |
        Q(person_id__icontains=search_query) |
        Q(person_email__icontains=search_query) |
        Q(person_phone__icontains=search_query) |
        Q(book__in=title) |
        Q(book__accession_number__icontains=search_query)

    )

    return books, search_query



def paginateBooks(request, books, results):
    page = request.GET.get('page')
    paginator = Paginator(books, results)

    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        books = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        books = paginator.page(page)

    leftIndex = (int(page)-4)
    if leftIndex < 1:
        leftIndex = 1
    rightIndex = (int(page)+5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return books, custom_range, paginator