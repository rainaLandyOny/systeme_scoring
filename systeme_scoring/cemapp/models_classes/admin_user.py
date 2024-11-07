from django.db import models
from .custom_user import CustomUser

class Admin(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Admin {self.user.username}"