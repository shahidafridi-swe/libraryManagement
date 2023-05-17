from django.shortcuts import redirect, render
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Librarian
from .forms import CustomUserCreationForm

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


@user_passes_test(lambda u: u.is_superuser)
def registerUser(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.institute_id = form.cleaned_data['institute_id']
            user.save()

            messages.success(request, 'User account has created successfully ! ')
            return redirect('librarians')
        else:
            messages.error(request, 'An error has occured in registration. Try again with correct information. ')
    context = {
        'form': form
    }
    return render(request, 'librarians/librarian-register.html', context)


@login_required(login_url='login')
def account(request):
    librarian = request.user.librarian
    context = {
        'librarian':librarian
    }
    return render(request, 'librarians/account.html', context)