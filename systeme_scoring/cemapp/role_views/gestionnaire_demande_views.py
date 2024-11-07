from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

def is_gestionnaire_demande(user):
    return user.role == 'gestionnaire_demande'

@login_required
@user_passes_test(is_gestionnaire_demande)
def gestionnaire_home(request):
    return render(request, 'gestionnaire_demande/gestionnaire_demande_home.html')
