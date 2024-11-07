from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    role_choices = [
        ('admin', 'Admin'),
        ('service_client', 'Service Client'),
        ('gestionnaire', 'Gestionnaire des Demandes'),
    ]
    role = models.CharField(max_length=20, choices=role_choices, default='service_client')

    def __str__(self):
        return self.username
