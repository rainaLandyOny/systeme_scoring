from django.db import models
from .custom_user import CustomUser
from .demande_credit import DemandeCredit
import uuid
from datetime import datetime, timedelta

class RendezvousFinalisation(models.Model):
    analyste = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    demande = models.ForeignKey(DemandeCredit, on_delete=models.CASCADE)
    date_debut_rendezvous = models.DateTimeField()
    date_fin_rendezvous = models.DateTimeField()
    termine = models.BooleanField(default=False)
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    modification_count = models.PositiveIntegerField(default=0)
    
def __str__(self):
        return self.lieu
    
def is_modifiable(self):
        now = datetime.now()
        return self.modification_count < 1 and self.date_debut_rendezvous - timedelta(days=3) > now