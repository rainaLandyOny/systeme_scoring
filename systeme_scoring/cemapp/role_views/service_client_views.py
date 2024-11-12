from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from ..models_classes.type_credit import TypeCredit
from ..models_classes.document_credit import DocumentCredit 
from ..models_classes.sous_types_credit import SousTypeCredit
from ..utils.role_checker import role_required

def is_service_client(user):
    return user.role == 'service_client'

@login_required
@role_required('service_client')
def service_home(request):
    return render(request, 'service_client/service_client_home.html')

@login_required
@role_required('service_client')
def liste_offres_credit(request):
    offres_credit = TypeCredit.objects.all()
    return render(request, 'liste_offres_credit.html', {'offres_credit': offres_credit})

@login_required
@role_required('service_client')
def offres_credit(request):
    type_credits = TypeCredit.objects.prefetch_related('soustypecredit_set').all()
    if request.user.is_authenticated:
        client_status = 'Nouveau' if hasattr(request.user, 'profile') and request.user.profile.client_status == 'Nouveau' else 'Ancien'
        documents = DocumentCredit.objects.filter(client_status=client_status)
    else:
        documents = []

    return render(request, 'service_client/offres_credit.html', {
        'type_credits': type_credits,
        'documents': documents,
    })
    
@login_required
@role_required('service_client')
def simulation_view(request, sous_type_id):
    sous_type = get_object_or_404(SousTypeCredit, id=sous_type_id)
    return render(request, 'service_client/simulation_offre.html', {'sous_type': sous_type})