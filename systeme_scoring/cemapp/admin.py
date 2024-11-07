from django.contrib import admin
from .models import CustomUser, Admin, ServiceClient, GestionnaireDemande

admin.site.register(CustomUser)
admin.site.register(Admin)
admin.site.register(ServiceClient)
admin.site.register(GestionnaireDemande)