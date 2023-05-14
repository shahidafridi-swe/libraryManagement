from django.shortcuts import render
from .models import Librarians


def librarians(request):
    librarians = Librarians.objects.all()
    context = {
        'librarians': librarians
    }
    return render(request, 'librarians/librarians.html', context)