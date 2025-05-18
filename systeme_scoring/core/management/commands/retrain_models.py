from django.core.management.base import BaseCommand
from ml_models import retrain_all_models

class Command(BaseCommand):
    help = 'Lance le réentraînement manuel des modèles'

    def handle(self, *args, **options):
        self.stdout.write("Début du réentraînement manuel...")
        retrain_all_models()
        self.stdout.write(self.style.SUCCESS("Réentraînement terminé avec succès !"))