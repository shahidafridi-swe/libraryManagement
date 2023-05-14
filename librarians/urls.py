from django.urls import path
from . import views

urlpatterns = [
    path('', views.librarians, name='librarians'),
]