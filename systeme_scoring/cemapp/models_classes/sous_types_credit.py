from django.db import models
from .type_credit import TypeCredit

class SousTypeCredit(models.Model):
    type_credit = models.ForeignKey(TypeCredit, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    description = models.TextField()
    montant_min = models.DecimalField(max_digits=12, decimal_places=2, default=300000)
    montant_max = models.DecimalField(max_digits=12, decimal_places=2)
    duree_min = models.IntegerField()
    duree_max = models.IntegerField()
    taux_interet = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return f"{self.nom} - {self.type_credit.nom}"