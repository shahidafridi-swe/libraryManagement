from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Librarian


# @receiver(post_save,sender=Librarian)
def createProfile(sender, instance, created, **kwargs):
    if created:
        user =instance
        librarian = Librarian.objects.create(
            user =user,
            username = user.username,
            email = user.email,
            name = user.first_name,
            institute_id = user.institute_id,
        )
post_save.connect(createProfile, sender=User)


def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()

post_delete.connect(deleteUser, sender=Librarian)