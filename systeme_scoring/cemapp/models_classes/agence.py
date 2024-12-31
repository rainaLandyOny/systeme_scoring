from django.db import models

class Agence(models.Model):
    lieu = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=13)
    capitale_total = models.DecimalField(max_digits=12, decimal_places=2)
    
def __str__(self):
        return self.lieu