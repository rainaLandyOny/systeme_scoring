from datetime import timedelta
from django.db import models
from django.utils.timezone import now
from .demande_credit import DemandeCredit

class RemboursementCredit(models.Model):
    TYPE_CHOICES = [
        ('normal', 'Normal'),
        ('anticipe', 'Remboursement anticipé'),
    ]
    
    demande = models.ForeignKey(DemandeCredit,on_delete=models.CASCADE,related_name='remboursements')
    date_paiement = models.DateTimeField(default=now)
    somme_paye = models.DecimalField(max_digits=10, decimal_places=2)
    numero_paiement = models.IntegerField()
    type_paiement = models.CharField( max_length=20, choices=TYPE_CHOICES, default='normal', null=False, blank=False)

    class Meta:
        ordering = ['numero_paiement']
        unique_together = ('demande', 'numero_paiement')

    def __str__(self):
        return f"Remboursement {self.numero_paiement} - {self.demande.numero_credit}"

    def montant_restant(self):
        total_paye = sum(remb.somme_paye for remb in self.demande.remboursements.all())
        return self.demande.montant_total - total_paye

    def est_en_retard(self):
        date_echeance = self.demande.date_creation + timedelta(days=30 * self.numero_paiement)
        return self.date_paiement > date_echeance