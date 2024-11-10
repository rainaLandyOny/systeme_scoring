from django.db import models

class Client(models.Model):
    matricule = models.CharField(max_length=10, unique=True)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    date_naissance = models.DateField()
    adresse = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    telephone = models.CharField(max_length=10)
    n_cin = models.CharField(max_length=12)
    statut_familial = models.CharField(max_length=50)
    nbr_dependant = models.IntegerField(blank=True, null=True)
    situation_professionnelle = models.CharField(max_length=50)
    titre_emploie = models.CharField(max_length=100, blank=True, null=True)
    nom_employeur = models.CharField(max_length=255, blank=True, null=True)
    duree_emploie = models.IntegerField(blank=True, null=True)
    revenu_mensuel = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    depense_mensuelles = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    dettes_existantes = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    situation_bancaire = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.matricule})"
