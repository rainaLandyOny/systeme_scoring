import csv
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.db.models import Sum, Count, Q
from ..models_classes.demande_credit import DemandeCredit
from ..models_classes.client import Client
from ..models_classes.custom_user import CustomUser
from ..models_classes.remboursement_credit import RemboursementCredit
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models.functions import TruncMonth, TruncDay

def is_directeur_agence(user):
    return user.role == 'directeur_agence'

@login_required
@user_passes_test(is_directeur_agence)
def directeur_home(request):
    now = datetime.now()
    debut_mois = datetime(now.year, now.month, 1)
    
    total_clients = Client.objects.count()

    demandes_mois = DemandeCredit.objects.filter(date_derniere_maj__gte=debut_mois)
    demandes_en_attente_inspection = demandes_mois.filter(statut_demande="en_attente_inspection").count()
    demandes_en_attente = demandes_mois.filter(statut_demande="en_attente_validation").count()
    demandes_signature = demandes_mois.filter(statut_demande="en_attente_signature").count()
    demandes_approuvees = demandes_mois.filter(statut_demande="approuvee").count()
    demandes_rejetees = demandes_mois.filter(statut_demande="rejete").count()
    
    remboursements_mois = RemboursementCredit.objects.filter(date_paiement__gte=debut_mois)    

    montant_emprunte = demandes_mois.filter(statut_demande="approuvee").aggregate(Sum("montant_total"))["montant_total__sum"] or 0
    benefice_mois = remboursements_mois.aggregate(Sum("somme_paye"))["somme_paye__sum"] or 0

    context = {
        "total_clients": total_clients,
        "demandes_en_attente_inspection": demandes_en_attente_inspection,
        "demandes_en_attente": demandes_en_attente,
        "demandes_signature": demandes_signature,
        "demandes_approuvees": demandes_approuvees,
        "demandes_rejetees": demandes_rejetees,
        "montant_emprunte": montant_emprunte,
        "benefice_mois": benefice_mois,
    }
    return render(request, "directeur_agence/directeur_home.html", context)

@login_required
@user_passes_test(is_directeur_agence)
def performance_generale(request):
    year = request.GET.get("year", datetime.now().year)
    month = request.GET.get("month", None)
    
    years = list(range(year, 1917, -1))

    return render(request, 'directeur_agence/performance_generale.html', {"year": year, "month": month, "years": years})


def format_labels(data, group_by):
    if group_by == TruncDay:
        return [entry["period"].strftime("%d-%m-%Y") for entry in data]
    return [entry["period"].strftime("%B %Y") for entry in data]

def get_performance_generale(request):
    year = request.GET.get("year")
    month = request.GET.get("month")

    base_filters = Q()
    remboursements_base_filters = Q()
    group_by = TruncMonth("date_derniere_maj")
    remboursements_group_by = TruncMonth("date_paiement")

    if year:
        base_filters &= Q(date_derniere_maj__year=year)
        remboursements_base_filters &= Q(date_paiement__year=year)
    if month:
        base_filters &= Q(date_derniere_maj__month=month)
        remboursements_base_filters &= Q(date_paiement__month=month)
        group_by = TruncDay("date_derniere_maj")
        remboursements_group_by = TruncDay("date_paiement")

    emprunts_data = (
        DemandeCredit.objects.filter(base_filters)
        .annotate(period=group_by)
        .values("period")
        .annotate(total=Sum("montant_total"))
        .order_by("period")
    )

    remboursements_data = (
        RemboursementCredit.objects.filter(remboursements_base_filters)
        .annotate(period=remboursements_group_by)
        .values("period")
        .annotate(total=Sum("somme_paye"))
        .order_by("period")
    )

    labels = format_labels(emprunts_data, group_by)
    emprunts = [entry["total"] for entry in emprunts_data]
    remboursements = [entry["total"] for entry in remboursements_data]

    status_dist = (
        DemandeCredit.objects.filter(base_filters)
        .values("statut_demande")
        .annotate(total=Count("statut_demande"))
    )

    data = {
        "emprunts_vs_remboursements": {
            "labels": labels,
            "emprunts": emprunts,
            "remboursements": remboursements,
        },
        "status_distribution": list(status_dist),
    }
    return JsonResponse(data)

@login_required
@user_passes_test(is_directeur_agence)
def performance_employes(request):
    year = request.GET.get("year", datetime.now().year)
    month = request.GET.get("month", None)
    
    years = list(range(year, 1917, -1))

    return render(request, 'directeur_agence/performance_analyste.html', {"year": year, "month": month, "years": years})

def get_performance_employes(request):
    annee = request.GET.get('annee')
    mois = request.GET.get('mois')
    
    filtre = Q()
    
    if annee:
        filtre &= Q(date_derniere_maj__year=int(annee))
    if mois:
        filtre &= Q(date_derniere_maj__month=int(mois))
    
    data = DemandeCredit.objects.filter(filtre).values(
        'traite_par__username'
    ).annotate(
        total=Count('id'),
        approuve=Count('id', filter=Q(statut_demande='approuve')),
        rejete=Count('id', filter=Q(statut_demande='rejete')),
        en_attente=Count('id', filter=Q(statut_demande='en_attente_validation'))
    ).order_by('-total')
    
    response_data = {
        "labels": [item['traite_par__username'] for item in data],
        "totals": [item['total'] for item in data],
        "approuves": [item['approuve'] for item in data],
        "rejetes": [item['rejete'] for item in data],
        "en_attente": [item['en_attente'] for item in data],
    }
    
    return JsonResponse(response_data)

@login_required
@user_passes_test(is_directeur_agence)
def gestion_employes(request):
    agence_directeur = request.user.agence
    
    roles_autorises = ['service_client', 'gestionnaire', 'analyste_demande']
    
    employes = CustomUser.objects.filter(
        agence=agence_directeur,
        role__in=roles_autorises
    ).order_by('role', 'username')
    
    roles = CustomUser.objects.filter(role__in=roles_autorises).values_list('role', flat=True).distinct()
    
    return render(request, 'directeur_agence/gestion_employes.html', {
        "employes": employes,
        "roles": roles
    })
    
@login_required
@user_passes_test(is_directeur_agence)
def save_employe(request):
    if request.method == "POST":
        employe_id = request.POST.get('id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        role = request.POST.get('role')

        # Vérifier si un employé existe (modification)
        if employe_id:
            employe = get_object_or_404(CustomUser, id=employe_id)
            employe.username = username
            employe.email = email
            employe.role = role
            employe.save()
            return JsonResponse({"success": True, "message": "Employé modifié avec succès"})
        else:
            # Ajouter un nouvel employé
            agence_directeur = request.user.agence
            CustomUser.objects.create(
                username=username,
                email=email,
                role=role,
                agence=agence_directeur
            )
            return JsonResponse({"success": True, "message": "Nouvel employé ajouté avec succès"})
    return JsonResponse({"success": False, "errors": "Méthode non autorisée"})