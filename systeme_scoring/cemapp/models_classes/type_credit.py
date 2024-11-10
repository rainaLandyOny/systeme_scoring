from django.db import models

class TypeCredit(models.Model):
    nom = models.CharField(max_length=50)
    duree_min = models.IntegerField()
    duree_max = models.IntegerField()
    montant_max = models.IntegerField()
    taux_mensuel = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom
