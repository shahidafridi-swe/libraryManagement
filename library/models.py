from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid
from librarians.models import Librarian


class Book(models.Model):
    BRANCH_CHOICE = [
        ('GULSHAN', 'Gulshan'),
        ('BARIDAHRA', 'Baridhara'),
        ('BANANI', 'Banani'),
    ]

    accession_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(99999)], unique=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    publish_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9999)], null=True, blank=True)
    edition = models.CharField(max_length=255, null=True, blank=True)
    ISBN = models.CharField(max_length=13, null=True, blank=True)
    call_number = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    page = models.PositiveIntegerField()
    branch = models.CharField(
        max_length=10, choices=BRANCH_CHOICE, default='GULSHAN' , blank=True, null=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    tags = models.CharField(max_length=255, null=True, blank=True)
    cover_photo = models.ImageField(
        default='default-book.png', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['accession_number']


class BookIssue(models.Model):
    PERSON_TYPE_CHOICES = [
        ("STUDENT", "Student"),
        ("FACULTY", "Faculty"),
    ]
    librarian = models.ForeignKey(Librarian, on_delete=models.PROTECT, null=True, blank=True)
    book = models.OneToOneField(
        Book, on_delete=models.PROTECT, null=True, blank=True)
    person_name = models.CharField(max_length=255)
    person_id = models.CharField(max_length=9, unique=True)
    person_type = models.CharField(
        max_length=7, choices=PERSON_TYPE_CHOICES, default="STUDENT")
    person_email = models.EmailField(max_length=255, unique=True)
    person_phone = models.CharField(max_length=11, blank=True, null=True)
    issued_date = models.DateField(auto_now_add=True)
    return_date = models.DateField()
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.person_name
    
    class Meta:
        ordering = ['return_date']


class NoticeBoard(models.Model):
    notice = models.TextField(blank=True, null=True)
    last_update = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

