from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Librarian


def librarians(request):
    librarians = Librarian.objects.all()
    context = {
        'librarians': librarians
    }
    return render(request, 'librarians/librarians.html', context)


def loginUser(request):

    if request.user.is_authenticated:
        return redirect('books')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('books')
        else:
            messages.error(request,"Password is incorrect")

    return render(request, 'librarians/login.html')


def logoutUser(request):
    logout(request)
    messages.error(request,"Librarian is looged out successfully !")
    return redirect('login')
