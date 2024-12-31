

def role_based_template(request):
    if request.user.is_authenticated:
        role = request.user.role
        if role == 'admin':
            return {'base_template': 'admin/base_admin.html'}
        elif role == 'directeur_agence':
            return {'base_template': 'directeur_agence/base_directeur_agence.html'}
        elif role == 'analyste_demande':
            return {'base_template': 'analyste_demande/base_analyste_demande.html'}
        elif role == 'gestionnaire':
            return {'base_template': 'gestionnaire_demande/base_gestionnaire_demande.html'}
        elif role == 'service_client':
            return {'base_template': 'service_client/base_service_client.html'}
        elif role == 'agent_inspection':
            return {'base_template': 'agent_inspection/base_agent_inspection.html'}
    return {'base_template': 'base.html'}
