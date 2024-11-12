

def role_based_template(request):
    if request.user.is_authenticated:
        role = request.user.role
        if role == 'admin':
            return {'base_template': 'admin/base_admin.html'}
        elif role == 'gestionnaire':
            return {'base_template': 'gestionnaire_demande/base_gestionnaire_demande.html'}
        elif role == 'service_client':
            return {'base_template': 'service_client/base_service_client.html'}
    return {'base_template': 'base.html'}
