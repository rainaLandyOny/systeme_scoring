from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
import joblib
from ..models_classes.demande_credit import DemandeCredit
from ..models_classes.client import Client
from random import choice, randint, uniform
from datetime import datetime, timedelta
from decimal import Decimal
from django.http import JsonResponse
import numpy as np
import pandas as pd

def is_admin(user):
    return user.role == 'admin'

@login_required
@user_passes_test(is_admin)
def admin_home(request):
    demandes_en_attente = DemandeCredit.objects.filter(statut_demande='en_attente').order_by('-date_demande')

    paginator = Paginator(demandes_en_attente, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'admin/admin_home.html', context)