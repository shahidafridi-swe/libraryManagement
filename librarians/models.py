from django.db import models
from django.contrib.auth.models import User
import uuid
class Librarians(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255,blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True, unique=True)
    username = models.CharField(max_length=255, blank=True, null=True, unique=True)
    institute_id = models.CharField(max_length=9, blank=True, null=True, unique=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.username
    