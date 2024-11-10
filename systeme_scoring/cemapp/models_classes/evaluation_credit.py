from django.db import models
from models_classes.demande_credit import DemandeCredit
from datetime import date

class EvaluationCredit(models.Model):
    demande_credit = models.ForeignKey(DemandeCredit, on_delete=models.CASCADE)
    score_calculé = models.FloatField()
    ratio_endettement = models.FloatField()
    date_decision = models.DateField(default=date.today)
    statut_final = models.CharField(max_length=50, choices=[('approuve', 'Approuvé'), ('rejete', 'Rejeté')])
    motif_rejet = models.TextField(null=True, blank=True)
    montant_accorde = models.FloatField(null=True, blank=True)
    analyste_decision = models.CharField(max_length=255, null=True, blank=True)  # Nom de l'analyste
    justification_analyste = models.TextField(null=True, blank=True)  # Explication additionnelle
