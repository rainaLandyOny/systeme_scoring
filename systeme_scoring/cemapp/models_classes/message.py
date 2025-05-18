from django.db import models
from .custom_user import CustomUser

class Messagerie(models.Model):
    expediteur = models.ForeignKey(CustomUser, related_name='messages_envoyes', on_delete=models.CASCADE)
    destinataire = models.ForeignKey(CustomUser, related_name='messages_recus', on_delete=models.CASCADE)
    contenu = models.TextField(default=' ')
    date_envoi = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)