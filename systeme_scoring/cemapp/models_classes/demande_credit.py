from django.db import models
from .client import Client
from .type_credit import TypeCredit

class DemandeCredit(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('approuve', 'Approuvé'),
        ('rejete', 'Rejeté')
    ]

    numero_credit = models.CharField(max_length=10, unique=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    type_credit = models.ForeignKey(TypeCredit, on_delete=models.CASCADE)
    duree = models.IntegerField()
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)
    montant_payer_mois = models.DecimalField(max_digits=10, decimal_places=2)
    motif_credit = models.TextField()
    date_demande = models.DateField(auto_now_add=True)
    statut_demande = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')

    def __str__(self):
        return f"Demande {self.numero_credit} - {self.client}"
