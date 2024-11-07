from django.contrib import admin
from .models_classes.custom_user import CustomUser
from .models_classes.admin_user import Admin
from .models_classes.service_client_user import ServiceClient
from .models_classes.gestionnaire_demande_user import GestionnaireDemande

admin.site.register(CustomUser)
admin.site.register(Admin)
admin.site.register(ServiceClient)
admin.site.register(GestionnaireDemande)