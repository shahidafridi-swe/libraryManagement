from django.contrib import admin
from .models import Book,BookIssue,NoticeBoard


admin.site.register(Book)
admin.site.register(BookIssue)
admin.site.register(NoticeBoard)