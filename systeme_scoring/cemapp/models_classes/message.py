from django.utils import timezone
from django.db import models
from .custom_user import CustomUser

class Messagerie(models.Model):
    expediteur = models.ForeignKey(CustomUser, related_name='messages_envoyes', on_delete=models.CASCADE)
    destinataire = models.ForeignKey(CustomUser, related_name='messages_recus', on_delete=models.CASCADE)
    contenu = models.TextField(default=' ')
    date_envoi = models.DateTimeField(default=timezone.now)
    lu = models.BooleanField(default=False)