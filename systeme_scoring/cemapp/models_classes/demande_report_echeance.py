from django.db import models
from .demande_credit import DemandeCredit

class DemandeReportEcheance(models.Model):
    numero_demande_report = models.CharField(max_length=20, unique=True)
    demande_credit = models.ForeignKey(DemandeCredit, on_delete=models.CASCADE)
    raison_report = models.TextField()
    date_report = models.DateField()