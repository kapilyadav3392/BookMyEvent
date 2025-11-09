from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    ROLE_CHOICES = (
        ("organizer", "Organizer"),
        ("attendee", "Attendee"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)


    def is_organizer(self):
        return self.role == "organizer"

    def is_attendee(self):
        return self.role == "attendee"
