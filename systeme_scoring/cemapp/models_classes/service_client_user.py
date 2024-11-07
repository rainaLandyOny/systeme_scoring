from django.db import models
from .custom_user import CustomUser

class ServiceClient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"Service Client {self.user.username}"
