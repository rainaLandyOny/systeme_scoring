from django.contrib import admin
from django.urls import path
from cemapp import views as baseviews
from cemapp.role_views import admin_views, service_client_views, gestionnaire_demande_views

urlpatterns = [
    path('superuser/', admin.site.urls),
    path('', baseviews.user_login, name='login'),
    path('logout/', baseviews.user_logout, name='logout'),
    path('admin/', admin_views.admin_home, name='admin_home'),
    path('gestionnairedemande/', gestionnaire_demande_views.gestionnaire_home, name='gestionnaire_home'),
    # service_client
    path('serviceclient/offres-credit/', service_client_views.offres_credit, name='offre_credit'),
    path('serviceclient/simulation/<int:sous_type_id>/', service_client_views.simulation_view, name='simulation_offre'),    
]
