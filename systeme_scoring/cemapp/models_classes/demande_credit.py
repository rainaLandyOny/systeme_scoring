from django.db import models
from .client import Client
from .sous_types_credit import SousTypeCredit

class DemandeCredit(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_attente_signature', 'En attente de signature'),
        ('approuve', 'Approuvé'),
        ('rejete', 'Rejeté'),
        ('termine', 'Terminé'),
    ]

    numero_credit = models.CharField(max_length=20, unique=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    sous_type_credit = models.ForeignKey(SousTypeCredit, on_delete=models.CASCADE)  # Remplacement
    duree = models.IntegerField()
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)
    montant_payer_mois = models.DecimalField(max_digits=10, decimal_places=2)
    motif_credit = models.TextField()
    date_demande = models.DateField(auto_now_add=True)
    statut_demande = models.CharField( max_length=20, choices=STATUT_CHOICES, default='en_attente', null=False, blank=False)
    date_derniere_maj = models.DateField(auto_now_add=True)
    
    def get_statut_display(self):
        return dict(self.STATUT_CHOICES).get(self.statut_demande, "Statut inconnu")
    
    def est_modifiable(self):
        return self.statut_demande == 'en_attente'
    
    def est_payable(self):
        return self.statut_demande == 'approuve'
    
    def __str__(self):
        return f"Demande {self.numero_credit} - {self.client}"
