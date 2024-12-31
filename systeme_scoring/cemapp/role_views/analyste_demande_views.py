import json
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
import joblib
from sklearn.base import ClassifierMixin, RegressorMixin
from sklearn.metrics import f1_score, mean_squared_error, precision_score, recall_score,accuracy_score,r2_score
from systeme_scoring import settings
from ml_models.model_manager import ModelManager
from ..models_classes.rendezvous_finalisation import RendezvousFinalisation
from ..models_classes.demande_credit import DemandeCredit
from ..models_classes.client import Client
from random import choice, randint, uniform
from datetime import datetime, timedelta
from decimal import Decimal
from django.http import HttpResponse, JsonResponse
import numpy as np
import pandas as pd
from django.core.mail import send_mail

def is_analyste(user):
    return user.role == 'analyste_demande'

@login_required
@user_passes_test(is_analyste)
def analyste_home(request):
    demandes_en_attente = DemandeCredit.objects.filter(statut_demande='en_attente_validation').order_by('-date_demande')

    paginator = Paginator(demandes_en_attente, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'analyste_demande/analyste_home.html', context)

@login_required
@user_passes_test(is_analyste)
def details_demande(request, demande_id):
    demande = get_object_or_404(DemandeCredit,id=demande_id)
    client = demande.client
    scores_dict = demande.get_scoring_client(request.user)

    return render(request, "analyste_demande/details_scoring_demande.html", {"client": client, "demande": demande, "scores": scores_dict})


def feature_importance_page(request):
    """
    Affiche la page de modification des importances des colonnes.
    """
    return render(request, "analyste_demande/importance_modele.html")

def get_feature_importances(request):
    """
    Charge l'importance des colonnes et les métriques d'un modèle pour un utilisateur connecté.
    """
    model_key = request.GET.get("model_key")
    if not model_key:
        return JsonResponse({"error": "Model key is required."}, status=400)

    user = request.user  # Utilisateur connecté

    try:
        model_manager = ModelManager()
        model = model_manager.load_model(model_key, user)

        # Récupérer les métriques sauvegardées
        metrics = getattr(model, "metrics_", None)
        if metrics is None:
            return JsonResponse({"error": "Metrics are not available for the selected model."}, status=400)

        # Récupérer l'importance des caractéristiques si disponible
        if hasattr(model, "feature_importances_"):
            feature_importances = model.feature_importances_
            feature_names = model.feature_names_in_ if hasattr(model, "feature_names_in_") else [
                f"Feature {i}" for i in range(len(feature_importances))
            ]

            data = [
                {"feature": name, "importance": float(importance)}
                for name, importance in zip(feature_names, feature_importances)
            ]
        else:
            data = []

        # Réponse JSON structurée
        return JsonResponse({
            "data": data,
            "metrics": metrics
        })

    except FileNotFoundError as e:
        return JsonResponse({"error": str(e)}, status=404)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)

def update_feature_importances(request):
    """
    Met à jour les importances des colonnes pour un utilisateur connecté et un modèle donné.
    """
    if request.method == "POST":
        model_key = request.POST.get("model_key", None)
        updated_importances = request.POST.get("updated_importances", None)

        if not model_key or not updated_importances:
            return JsonResponse({"error": "Model key and updated importances are required."}, status=400)

        try:
            model_manager = ModelManager()
            user = request.user  # Utilisateur connecté
            model = model_manager.load_model(model_key, user)

            # Mettre à jour les importances
            updated_importances = json.loads(updated_importances)  # Convertir le JSON en dictionnaire
            for i, feature in enumerate(model.feature_names_in_):
                if feature in updated_importances:
                    model.feature_importances_[i] = updated_importances[feature]

            # Sauvegarder le modèle modifié dans le cache utilisateur
            model_manager.update_model_cache(user.id, model_key, model)
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)


@login_required
@user_passes_test(is_analyste)
def create_rendezvous(request, demande_id):
    demande = get_object_or_404(DemandeCredit, id=demande_id)

    if demande.statut != "en_attente_validation":
        messages.error(request, "Cette demande n'est pas en attente.")
        return redirect("detail_demande", demande_id=demande_id)

    if request.method == "POST":
        datetime_debut = request.POST.get("date_debut_rendezvous")
        datetime_fin = request.POST.get("date_fin_rendezvous")

        if datetime_debut >= datetime_fin:
            messages.error(request, "La date de fin doit être postérieure à la date de début.")
            return redirect("detail_demande", demande_id=demande_id)

        rendezvous = RendezvousFinalisation.objects.create(
            demande=demande,
            analyste=request.user,
            datetime_debut=datetime_debut,
            datetime_fin=datetime_fin,
        )
        rendezvous.save()

        demande.statut = "en_attente_signature"
        demande.save()

        email_subject = "Notification de Rendez-vous"
        email_message = (
            f"Bonjour {demande.client.nom} {demande.client.prenom},\n\n"
            f"Suite à votre demande de crédit: {demande.numero_credit} , une entrevue avec un de nos analyste des demandes sera prévu pour :\n"
            f"- Date et heure de début : {datetime_debut}\n"
            f"- Date et heure de fin : {datetime_fin}\n\n"
            f"Merci de bien vouloir respecter cet horaire. Si vous avez des questions, veuillez nous contacter par email ou par téléphone."
            f"Cordialement,\n"
        )
        try:
            send_mail(
                email_subject,
                email_message,
                settings.EMAIL_HOST_USER,
                ['henintsoa404@gmail.com'],
            )
            messages.success(request, "Rendez-vous créé et email envoyé au client.")
        except Exception as e:
            messages.error(request, f"Le rendez-vous a été créé, mais l'envoi de l'email a échoué : {e}")

    return redirect("detail_demande", demande_id=demande_id)
    

@login_required
@user_passes_test(is_analyste)    
def refus_demande(request, demande_id):
    demande = DemandeCredit.objects.get(id=demande_id)

    if request.method == 'POST':
        raison_refus = request.POST.get('raisonRefus')

        demande.statut = "refusé"
        demande.raison_refus = raison_refus
        demande.save()

        email_subject = "Notification de Refus"
        email_message = (
            f"Bonjour {demande.client.nom} {demande.client.prenom},\n\n"
            f"Suite à votre demande de crédit: {demande.numero_credit} , nous vous informons que votre demande a été refusée pour la raison suivante :\n"
            f"{raison_refus}\n"
            f"Nous nous excusons pour la gêne occasionnelle et nous vous invitons à nous contacter si vous avez des questions.\n\n"
            f"Cordialement,\n"
        )
        try:
            send_mail(
                email_subject,
                email_message,
                settings.EMAIL_HOST_USER,
                ['henintsoa404@gmail.com'],
            )
            messages.success(request, "Demande refusée et email envoyé au client.")
        except Exception as e:
            messages.error(request, f"Demande refusée, mais l'envoi de l'email a échoué : {e}")

        return redirect('detail_demande', demande_id=demande_id)

    return HttpResponse("Erreur : méthode non autorisée", status=405)

@login_required
@user_passes_test(is_analyste)  
def liste_rendez_vous(request):
    rendezvous = RendezvousFinalisation.objects.filter(analyste=request.user).filter(termine=False).order_by('date_debut_rendezvous')

    paginator = Paginator(rendezvous, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    
    return render(request, "analyste_demande/liste_rendez_vous.html", {"rendezvous": context})

@login_required
@user_passes_test(is_analyste)  
def resume_demande_rendez_vous(request, rendezvous_id):
    rendezvous = get_object_or_404(RendezvousFinalisation, id=rendezvous_id)
    demande = rendezvous.demande
    client = demande.client
    scores_dict = demande.get_scoring_client(request.user)
    if(demande.sous_type_credit.type_credit.isCreditEntrepreneur):
        scores_dict + demande.get_scoring_inspection
    return render(request, "analyste_demande/details_scoring_demande.html", {"rendezvous": rendezvous, "client": client, "demande": demande, "scores": scores_dict})


def client_modifier_rendezvous(request, token):
    rendezvous = get_object_or_404(RendezvousFinalisation, token=token)

    if not rendezvous.is_modifiable():
        if rendezvous.modification_count >= 1:
            messages.error(request, "Vous avez déjà modifié ce rendez-vous une fois. Aucune autre modification n'est autorisée.")
        elif rendezvous.date_debut_rendezvous - timedelta(days=3) <= datetime.now():
            messages.error(request, "Le rendez-vous est dans moins de 3 jours. Il ne peut pas être modifié.")
        return redirect("home") 

    if request.method == "POST":
        new_date_debut = request.POST.get("date_debut_rendezvous")
        new_date_fin = request.POST.get("date_fin_rendezvous")

        if new_date_debut and new_date_fin:
            new_date_debut = datetime.fromisoformat(new_date_debut)
            new_date_fin = datetime.fromisoformat(new_date_fin)

            if new_date_debut >= new_date_fin:
                messages.error(request, "La date de fin doit être postérieure à la date de début.")
                return redirect("modify_rendezvous", token=rendezvous.token)

            rendezvous.date_debut_rendezvous = new_date_debut
            rendezvous.date_fin_rendezvous = new_date_fin
            rendezvous.modification_count += 1
            rendezvous.save()

            messages.success(request, "Le rendez-vous a été modifié avec succès.")
            return redirect("home")

    return render(request, "modify_rendezvous.html", {"rendezvous": rendezvous})

    