from django.db import models

class TypeCredit(models.Model):
    nom = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom
    
    def isCreditEntrepreneur(self):
        return self.nom == "Crédit aux entrepreneurs"
