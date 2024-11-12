from django.db import models

class DocumentCredit(models.Model):
    STATUS_CHOICES = [
        ('Nouveau', 'Nouveau Client'),
        ('Ancien', 'Ancien Client'),
    ]

    nom_document = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    client_status = models.CharField(max_length=50, choices=STATUS_CHOICES)

    def __str__(self):
        return self.nom_document
