from django.urls import path
from . import views

urlpatterns = [
    path('', views.librarians, name='librarians'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
]