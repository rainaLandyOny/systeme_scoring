from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

def is_service_client(user):
    return user.role == 'service_client'

@login_required
@user_passes_test(is_service_client)
def service_home(request):
    return render(request, 'service_client/service_client_home.html')
