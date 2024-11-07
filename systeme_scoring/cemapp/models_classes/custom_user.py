from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    role_choices = [
        ('admin', 'Admin'),
        ('service_client', 'Service Client'),
        ('gestionnaire', 'Gestionnaire des Demandes'),
    ]
    role = models.CharField(max_length=20, choices=role_choices, default='service_client')
    groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)

    def __str__(self):
        return self.username
