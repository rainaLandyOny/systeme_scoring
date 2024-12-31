from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from ..models_classes.demande_credit import DemandeCredit
from django.core.paginator import Paginator

def is_agent_inspection(user):
    return user.role == 'agent_inspection'

@login_required
@user_passes_test(is_agent_inspection)
def agent_inspection_home(request):
    demande_attente_inspection = DemandeCredit.objects.filter(statut_demande='en_attente_inspection').order_by('-date_demande')
    paginator = Paginator(demande_attente_inspection, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'agent_inspection/agent_inspection_home.html', context)

