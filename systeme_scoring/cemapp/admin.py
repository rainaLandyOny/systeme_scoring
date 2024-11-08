from django.contrib import admin
from .models_classes.custom_user import CustomUser

admin.site.register(CustomUser)