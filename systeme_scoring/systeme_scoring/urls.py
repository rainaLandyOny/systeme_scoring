"""
URL configuration for systeme_scoring project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from cemapp import views as baseviews
from cemapp.role_views import admin_views, service_client_views, gestionnaire_demande_views

urlpatterns = [
    path('superuser/', admin.site.urls),
    path('', baseviews.user_login, name='login'),
    path('admin/', admin_views.admin_home, name='admin_home'),
    path('gestionnairedemande/', gestionnaire_demande_views.gestionnaire_home, name='gestionnaire_home'),
    path('serviceclient/', service_client_views.service_home, name='service_home'),
]
