from django.db import models
from .demande_credit import DemandeCredit

class RemboursementCredit(models.Model):
    demande_credit = models.ForeignKey(DemandeCredit, on_delete=models.CASCADE)
    date_payement = models.DateTimeField()
    somme_paye = models.DecimalField(max_digits=10, decimal_places=2)
    n_payement = models.IntegerField()

    def __str__(self):
        return f"Remboursement {self.n_payement} - {self.demande_credit.numero_credit}"
